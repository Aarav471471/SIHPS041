from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.db import get_db
from app.models.all import User, Site, RoleEnum, Certificate, Attempt, CertStatusEnum, Module
from app.security import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

def require_admin_or_sup(user: User = Depends(get_current_user)):
    if user.role not in [RoleEnum.admin, RoleEnum.supervisor]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_sup)):
    workers_q = db.query(User).filter(User.role == RoleEnum.worker, User.is_active == True)
    if current_user.role == RoleEnum.supervisor:
        workers_q = workers_q.filter(User.site_id == current_user.site_id)
    
    total_workers = workers_q.count()
    worker_ids = [w.id for w in workers_q.all()]
    
    if not worker_ids:
        return {"total_workers": 0, "certified_pct": 0, "pass_rate": 0, "avg_score": 0, "expiring_30d": 0, "revoked": 0}
        
    valid_certs = db.query(Certificate).filter(
        Certificate.user_id.in_(worker_ids),
        Certificate.status == CertStatusEnum.valid,
        Certificate.expires_at > datetime.utcnow()
    ).count()
    
    certified_pct = (valid_certs / total_workers * 100) if total_workers > 0 else 0
    
    attempts = db.query(Attempt).filter(Attempt.user_id.in_(worker_ids))
    total_attempts = attempts.count()
    passed_attempts = attempts.filter(Attempt.passed == True).count()
    pass_rate = (passed_attempts / total_attempts * 100) if total_attempts > 0 else 0
    
    avg_score = db.query(func.avg(Attempt.server_score)).filter(Attempt.user_id.in_(worker_ids)).scalar() or 0
    
    thirty_days = datetime.utcnow() + timedelta(days=30)
    expiring = db.query(Certificate).filter(
        Certificate.user_id.in_(worker_ids),
        Certificate.status == CertStatusEnum.valid,
        Certificate.expires_at <= thirty_days,
        Certificate.expires_at > datetime.utcnow()
    ).count()
    
    revoked = db.query(Certificate).filter(
        Certificate.user_id.in_(worker_ids),
        Certificate.status == CertStatusEnum.revoked
    ).count()
    
    return {
        "total_workers": total_workers,
        "certified_pct": round(certified_pct, 1),
        "pass_rate": round(pass_rate, 1),
        "avg_score": round(avg_score, 1),
        "expiring_30d": expiring,
        "revoked": revoked
    }

@router.post("/certificates/{cid}/revoke")
def revoke_certificate(cid: str, reason: str, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    cert = db.query(Certificate).filter(Certificate.id == cid).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
        
    cert.status = CertStatusEnum.revoked
    cert.revoked_reason = reason
    cert.revoked_at = datetime.utcnow()
    
    from app.models.all import AuditLog
    db.add(AuditLog(
        actor_id=current_user.id,
        action="revoke_certificate",
        entity="certificate",
        entity_id=cid,
        meta_json=f'{{"reason": "{reason}"}}'
    ))
    db.commit()
    return {"status": "ok"}

@router.get("/compliance")
def get_compliance(db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_sup)):
    # Simple compliance matrix: site x module -> percentage
    sites = db.query(Site).all()
    modules = db.query(Module).all()
    
    if current_user.role == RoleEnum.supervisor:
        sites = [s for s in sites if s.id == current_user.site_id]
        
    matrix = []
    for s in sites:
        workers = db.query(User).filter(User.site_id == s.id, User.role == RoleEnum.worker, User.is_active == True).all()
        w_ids = [w.id for w in workers]
        if not w_ids:
            continue
            
        row = {"site_id": s.id, "site_name": s.name, "modules": {}}
        for m in modules:
            certs = db.query(Certificate).filter(
                Certificate.user_id.in_(w_ids),
                Certificate.module_code == m.code,
                Certificate.status == CertStatusEnum.valid,
                Certificate.expires_at > datetime.utcnow()
            ).count()
            row["modules"][m.code] = round((certs / len(w_ids) * 100), 1)
        matrix.append(row)
        
    return matrix

@router.get("/workers")
def get_workers(db: Session = Depends(get_db), current_user: User = Depends(require_admin_or_sup)):
    q = db.query(User).filter(User.role == RoleEnum.worker)
    if current_user.role == RoleEnum.supervisor:
        q = q.filter(User.site_id == current_user.site_id)
    
    workers = q.all()
    res = []
    for w in workers:
        certs = db.query(Certificate).filter(Certificate.user_id == w.id).all()
        site = db.query(Site).filter(Site.id == w.site_id).first()
        res.append({
            "id": w.id,
            "name": w.name,
            "worker_code": w.worker_code,
            "site_name": site.name if site else "N/A",
            "certificates": len(certs)
        })
    return res

@router.get("/analytics/timeline")
def get_timeline(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    # simple mock timeline
    from sqlalchemy import cast, Date
    attempts = db.query(cast(Attempt.submitted_at, Date).label("d"), func.count(Attempt.id)).group_by("d").all()
    return [{"date": str(d), "attempts": c} for d, c in attempts]
@router.get("/analytics/questions")
def get_hardest_questions(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    # Mock data for hardest questions
    return [
        {"question_id": "fire_q2", "miss_rate": 45.2, "module": "fire"},
        {"question_id": "gas_q5", "miss_rate": 38.1, "module": "gas"}
    ]

@router.get("/export/compliance.csv")
def export_compliance_csv(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return Response(content="site,module,compliance_pct\nDHN-01,fire,85.0\n", media_type="text/csv")

@router.get("/export/compliance.pdf")
def export_compliance_pdf(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    return Response(content="dummy_pdf_content", media_type="application/pdf")
