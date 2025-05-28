from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class IdentityData(BaseModel):
    email: EmailStr
    email_verified: bool
    phone_verified: bool
    sub: UUID


class Identity(BaseModel):
    id: UUID
    identity_id: UUID
    user_id: UUID
    identity_data: IdentityData
    provider: str
    created_at: datetime
    last_sign_in_at: datetime
    updated_at: datetime


class AppMetadata(BaseModel):
    provider: str
    providers: List[str]


class UserMetadata(BaseModel):
    email: EmailStr
    email_verified: bool
    phone_verified: bool
    sub: UUID


class CredentialsResponse(BaseModel):
    id: UUID
    app_metadata: AppMetadata
    user_metadata: UserMetadata
    aud: str
    confirmation_sent_at: Optional[datetime]
    recovery_sent_at: Optional[datetime]
    email_change_sent_at: Optional[datetime]
    new_email: Optional[EmailStr]
    new_phone: Optional[str]
    invited_at: Optional[datetime]
    action_link: Optional[str]
    email: EmailStr
    phone: str
    created_at: datetime
    confirmed_at: Optional[datetime]
    email_confirmed_at: Optional[datetime]
    phone_confirmed_at: Optional[datetime]
    last_sign_in_at: Optional[datetime]
    role: str
    updated_at: datetime
    identities: List[Identity]
    is_anonymous: bool
    factors: Optional[str]
