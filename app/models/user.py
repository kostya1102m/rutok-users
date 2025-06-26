from pydantic import BaseModel, EmailStr, Field, field_validator, validate_email
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    banned: bool
    username: str
    email: EmailStr
    phone: Optional[str] = None
    role_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
class UserAuth(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=30)
    email: Optional[EmailStr] = None
    hashed_password: str
    
class UserRegister(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    hashed_password: str
    
    @field_validator('email')
    @staticmethod
    def email_validation(cls, value):
        return validate_email(value)[1]
    
    # @field_validator('password')
    # @staticmethod
    # def password_validator(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("Пароль должен содержать не менее 8 символов")
    #     if not any(char.isdigit() for char in value):
    #         raise ValueError("Пароль должен содержать хотя бы одну цифру")
    #     if not any(char.isalpha() for char in value):
    #         raise ValueError("Пароль должен содержать хотя бы одну букву")
    #     if not any(char.isupper() for char in value):
    #         raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
    #     if not any(char in "!@#$%^&*()-_+=" for char in value):
    #         raise ValueError("Пароль должен содержать хотя бы один специальный символ (!@#$%^&*()-_+=)")
    #     return value

    @field_validator('username')
    @staticmethod
    def username_validator(cls, value):
        if not value:
            raise ValueError("Имя пользователя не может быть пустым")
        if not value.isalnum():
            raise ValueError("Имя пользователя должно содержать только буквы и цифры")
        if value.isdigit():
            raise ValueError("Имя пользователя не может состоять только из цифр")
        return value

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    hash_password: str
    phone: Optional[str] = None
    role_id: int
    created_at: datetime = datetime.now()


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=30)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=11, max_length=11)
    bio: Optional[str] = None
    avatar: Optional[bytes] = None
    
    @field_validator('email')
    @staticmethod
    def email_validation(cls, value):
        return validate_email(value)[1]
    
    @field_validator('phone')
    @staticmethod
    def phone_validation(cls, value):
        if not value.isdigit() or value[0] != "8":
            raise ValueError("Номер должен начинаться с 8 и содержать только цифры")
        return value
    
    @field_validator('username')
    @staticmethod
    def username_validator(cls, value):
        if not value:
            raise ValueError("Имя пользователя не может быть пустым")
        if not value.isalnum():
            raise ValueError("Имя пользователя должно содержать только буквы и цифры")
        if value.isdigit():
            raise ValueError("Имя пользователя не может состоять только из цифр")
        return value
        