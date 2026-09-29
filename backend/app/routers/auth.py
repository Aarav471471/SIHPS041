from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, LoginResponse, Token, UserResponse
from app.models.all import User, Site, RoleEnum
from app.security import get_password_hash, verify_password, create_access_token, create_refresh_token, get_current_user
import uuid

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    site = db.query(Site).filter(Site.code == req.site_code).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site code not found")
    
    if db.query(User).filter(User.phone == req.phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")
        
    hashed_pin = get_password_hash(req.pin)
    worker_code = f"W-{uuid.uuid4().hex[:6].upper()}"
    
    user = User(
        name=req.name,
        phone=req.phone,
        pin_hash=hashed_pin,
        language=req.language,
        site_id=site.id,
        role=RoleEnum.worker,
        worker_code=worker_code
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user or not verify_password(req.pin, user.pin_hash):
        raise HTTPException(status_code=401, detail="Invalid phone or PIN")
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return LoginResponse(
        token=Token(access_token=access_token, refresh_token=refresh_token),
        user=user
    )

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
