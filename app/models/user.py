from pydantic import BaseModel, EmailStr, Field, field_validator, validate_email
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    hash_password: str
    phone: Optional[str] = None
    role_id: int = 5 
    created_at: datetime = datetime.now()
    
    @field_validator('email')
    @staticmethod
    def email_validation(cls, value):
        return validate_email(value)[1]

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=30)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    role_id: Optional[int] = None
    
    @field_validator('email')
    @staticmethod
    def email_validation(cls, value):
        return validate_email(value)[1]

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: Optional[str]
    bio: Optional[str]
    avatar: Optional[str]
    banned: bool
    created_at: datetime
    updated_at: Optional[datetime]
    role_id: int
        