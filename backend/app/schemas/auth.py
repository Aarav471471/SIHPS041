from pydantic import BaseModel, Field
from typing import Optional
from app.models.all import RoleEnum, LanguageEnum

class UserBase(BaseModel):
    name: str
    phone: str
    language: LanguageEnum = LanguageEnum.en

class RegisterRequest(UserBase):
    pin: str = Field(..., min_length=4, max_length=4)
    site_code: str

class LoginRequest(BaseModel):
    phone: str
    pin: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    site_id: Optional[int]
    worker_code: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    token: Token
    user: UserResponse
