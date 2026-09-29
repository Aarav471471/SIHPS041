from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.all import Certificate, User, Site
from app.services.crypto_service import verify_signature

router = APIRouter(prefix="/verify", tags=["verify"])

@router.get("/{cid}")
def verify_cert(cid: str, d: str = Query(None), s: str = Query(None), db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(Certificate.id == cid).first()
    
    if not cert:
        return {"status": "NOT_FOUND"}
    
    # If client passed d (payload) and s (signature), we can verify them too
    sig_valid = True
    if d and s:
        sig_valid = verify_signature(d, s)
        if not sig_valid:
            return {"status": "TAMPERED"}
            
    worker = db.query(User).filter(User.id == cert.user_id).first()
    site = db.query(Site).filter(Site.id == worker.site_id).first() if worker else None
    
    return {
        "status": cert.status.value.upper(),
        "name": worker.name if worker else "Unknown",
        "modules": [cert.module_code],
        "issued": cert.issued_at,
        "expires": cert.expires_at,
        "site": site.code if site else "Unknown",
        "revoked_reason": cert.revoked_reason
    }
