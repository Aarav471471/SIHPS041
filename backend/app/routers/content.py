from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.all import ContentVersion, User
from app.security import get_current_user
import os
import zipfile
import tempfile
import hashlib

router = APIRouter(prefix="/content", tags=["content"])
CONTENT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "content")

@router.get("/version")
def get_version(db: Session = Depends(get_db)):
    # Always return 1 for demo purposes unless DB says otherwise
    cv = db.query(ContentVersion).order_by(ContentVersion.id.desc()).first()
    return {"version": cv.version if cv else 1, "hash": "dummy_hash"}

@router.get("/pack")
def get_pack(audio: int = 0, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Create a zip of the content folder
    if not os.path.exists(CONTENT_PATH):
        raise HTTPException(status_code=404, detail="Content folder not found")
        
    temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(CONTENT_PATH):
            for file in files:
                if not audio and 'audio' in root:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, CONTENT_PATH)
                zipf.write(file_path, arcname)
    
    temp_zip.close()
    return FileResponse(temp_zip.name, media_type="application/zip", filename="content.zip")
