from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class AmrEntry(BaseModel):
    method: str
    timestamp: int


class AppMetadata(BaseModel):
    provider: str
    providers: List[str]


class UserMetadata(BaseModel):
    email: EmailStr
    email_verified: bool
    phone_verified: bool
    sub: UUID


class TokenPayload(BaseModel):
    iss: str
    sub: UUID
    aud: str
    exp: int
    iat: int
    email: EmailStr
    phone: Optional[str] = ""
    app_metadata: AppMetadata
    user_metadata: UserMetadata
    role: str
    aal: str
    amr: List[AmrEntry]
    session_id: UUID
    is_anonymous: bool
