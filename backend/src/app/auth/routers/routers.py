from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from ..config.cfg import DEV_MODE
from ..models.token import TokenPayload
from ..models.users import (
    UserLogin,
    UserRegister,
    PasswordResetRequest,
    AuthTokens,
    UserCredentialsChangeRequest,
)
from ..services.services import (
    delete_all_cookies,
    login,
    logout,
    register,
    verify_token,
    send_password_reset,
    login_with_password_reset,
    change_email,
    change_password,
)

auth_router = APIRouter()
security = HTTPBearer()


@auth_router.post("/users")
async def sign_up(user: UserRegister, request: Request):
    return await register(user, request.state.sess)


@auth_router.post("/sessions")
async def sign_in(user: UserLogin):
    return await login(user)


@auth_router.delete("/sessions/")
async def sign_out(payload: TokenPayload = Depends(verify_token)):
    return await logout(payload)


@auth_router.get("/users/me")
async def get_current_user(payload: TokenPayload = Depends(verify_token)):
    return payload


@auth_router.post("/sessions/password-reset/request")
async def send_reset_link(user: PasswordResetRequest):
    return await send_password_reset(user)


@auth_router.post("/sessions/password-reset/login")
async def login_through_password_reset(tokens: AuthTokens):
    return await login_with_password_reset(tokens)


@auth_router.post("/update-password")
async def update_password(
    credentials: UserCredentialsChangeRequest,
    payload: TokenPayload = Depends(verify_token),
):
    return await change_password(payload, credentials)


@auth_router.post("/update-email")
async def update_email(
    credentials: UserCredentialsChangeRequest,
    payload: TokenPayload = Depends(verify_token),
):
    return await change_email(payload, credentials)


if DEV_MODE:

    @auth_router.delete("/delete_all_acookies")
    async def delete_auth_cookies():
        return await delete_all_cookies()
