from schemas.cfg import BaseConfig
from pydantic import EmailStr
from typing import Optional


class UserBase(BaseConfig):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr



class UserCreate(BaseConfig):
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr



class UserUpdate(BaseConfig):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
