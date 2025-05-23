from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str
    user_id: str