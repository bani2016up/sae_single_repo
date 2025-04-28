from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPBearer
from ..services.services import (
    verify_token,
    login,
    register,
    logout,
    give_account_info,
    delete_all_cookies,
)
from ..models.users import UserLogin, UserRegister
from fastapi.responses import JSONResponse


auth_router = APIRouter()
security = HTTPBearer()


@auth_router.post("/sign_up")
async def sign_up(user: UserRegister):
    return await register(user)


@auth_router.post("/sign_in")
async def sign_in(user: UserLogin):
    return await login(user)


@auth_router.delete("/sign_out")
async def sign_out(payload: dict = Depends(verify_token)):
    return await logout(payload)


@auth_router.get("/account_check")
async def check_account(payload: dict = Depends(verify_token)):
    return await give_account_info(payload)


# USE ONLY FOR DEBUGGING OR AS ЗАТЫЧКА ON BUGS
@auth_router.get("/delete_all_cookies")
async def delete_all_cookies():
    return await delete_all_cookies()
