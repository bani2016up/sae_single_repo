from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from ..config.cfg import DEV_MODE
from ..models.token import TokenPayload
from ..models.users import UserLogin, UserRegister
from ..services.services import (
    delete_all_cookies,
    give_account_info,
    login,
    logout,
    register,
    verify_token,
)

auth_router = APIRouter()
security = HTTPBearer()


@auth_router.post("/users")
async def sign_up(user: UserRegister):
    return await register(user)


@auth_router.post("/sessions")
async def sign_in(user: UserLogin):
    return await login(user)


@auth_router.delete("/sessions/")
async def sign_out(payload: TokenPayload = Depends(verify_token)):
    return await logout(payload)


@auth_router.get("/users/me")
async def get_current_user(payload: TokenPayload = Depends(verify_token)):
    return give_account_info(payload)


if DEV_MODE:

    @auth_router.get("/delete_all_cookies")
    async def delete_all_cookies():
        return await delete_all_cookies()
