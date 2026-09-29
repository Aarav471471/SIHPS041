from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db import get_db
from app.models.all import User, Attempt, AttemptAnswer, AttemptStep, Certificate, MicroQuizResult, CertStatusEnum, ContentVersion
from app.schemas.sync import SyncPushRequest, SyncPullResponse, CertResponse
from app.security import get_current_user
from app.services.grading_service import grade_attempt
from app.services.crypto_service import sign_payload
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/sync", tags=["sync"])

@router.post("/push")
def push_sync(req: SyncPushRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_certs = []
    
    for att_sync in req.attempts:
        # Check if attempt already exists
        existing = db.query(Attempt).filter(Attempt.id == att_sync.id).first()
        if existing:
            continue
            
        # Grade attempt
        answers_dict = [a.dict() for a in att_sync.answers]
        steps_dict = [s.dict() for s in att_sync.steps]
        
        grade_result = grade_attempt(att_sync.module_code, answers_dict, steps_dict)
        
        att = Attempt(
            id=att_sync.id,
            user_id=current_user.id,
            module_code=att_sync.module_code,
            started_at=att_sync.started_at,
            submitted_at=att_sync.submitted_at,
            device_id=att_sync.device_id,
            client_score=att_sync.client_score,
            app_version=att_sync.app_version,
            server_score=grade_result["server_score"],
            ar_score=grade_result["ar_score"],
            assess_score=grade_result["assess_score"],
            passed=grade_result["passed"]
        )
        db.add(att)
        
        # We should store answers/steps too in real code
        
        if grade_result["passed"]:
            # Check if user already has a valid cert for this module
            existing_cert = db.query(Certificate).filter(
                Certificate.user_id == current_user.id,
                Certificate.module_code == att_sync.module_code,
                Certificate.status == CertStatusEnum.valid
            ).first()
            
            if not existing_cert:
                import json
                issued = datetime.utcnow()
                expires = issued + timedelta(days=365)
                payload = {
                    "v": 1,
                    "cid": str(uuid.uuid4()),
                    "wid": current_user.worker_code,
                    "name": current_user.name,
                    "mods": [att_sync.module_code],
                    "score": grade_result["server_score"],
                    "iat": int(issued.timestamp()),
                    "exp": int(expires.timestamp()),
                    "site": current_user.site.code if current_user.site else "UNKNOWN"
                }
                
                sig = sign_payload(payload)
                cert = Certificate(
                    id=payload["cid"],
                    user_id=current_user.id,
                    module_code=att_sync.module_code,
                    attempt_id=att.id,
                    score=grade_result["server_score"],
                    issued_at=issued,
                    expires_at=expires,
                    status=CertStatusEnum.valid,
                    payload_json=json.dumps(payload, separators=(',', ':'), sort_keys=True),
                    signature_b64=sig
                )
                db.add(cert)
                db.flush()
                new_certs.append(cert)
    
    for mq in req.micro_quizzes:
        db.add(MicroQuizResult(
            user_id=current_user.id,
            module_code=mq.module_code,
            day_offset=mq.day_offset,
            score=mq.score,
            taken_at=mq.taken_at
        ))
        
    db.commit()
    return {"status": "ok", "new_certificates": len(new_certs)}

@router.get("/pull", response_model=SyncPullResponse)
def pull_sync(since: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    certs = db.query(Certificate).filter(Certificate.user_id == current_user.id).all()
    
    cv = db.query(ContentVersion).order_by(ContentVersion.id.desc()).first()
    version = cv.version if cv else 1
    
    cert_responses = []
    for c in certs:
        cert_responses.append(CertResponse(
            id=c.id,
            module_code=c.module_code,
            score=c.score,
            issued_at=c.issued_at,
            expires_at=c.expires_at,
            status=c.status.value,
            payload_json=c.payload_json,
            signature_b64=c.signature_b64
        ))
        
    return SyncPullResponse(
        certificates=cert_responses,
        content_version=version
    )
@router.get("/certificates/me", response_model=List[CertResponse])
def get_my_certs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    certs = db.query(Certificate).filter(Certificate.user_id == current_user.id).all()
    res = []
    for c in certs:
        res.append(CertResponse(
            id=c.id,
            module_code=c.module_code,
            score=c.score,
            issued_at=c.issued_at,
            expires_at=c.expires_at,
            status=c.status.value,
            payload_json=c.payload_json,
            signature_b64=c.signature_b64
        ))
    return res
