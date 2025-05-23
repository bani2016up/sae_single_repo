from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegisterResponse(BaseModel):
    message: str
    user_id: str


class PasswordResetResponse(BaseModel):
    email: str
    message: str


class PasswordResetRequest(BaseModel):
    email: str


class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class UserCredentialsChangeResponse(BaseModel):
    message: str
    new_email: Optional[EmailStr]
    new_password: Optional[str]


class UserCredentialsChangeRequest(BaseModel):
    new_email: Optional[EmailStr]
    new_password: Optional[str]
