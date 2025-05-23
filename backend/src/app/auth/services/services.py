import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from jose import JWTError, ExpiredSignatureError, jwt
from supabase import Client, create_client

from ..config.cfg import (
    ACCESS_TOKEN_MAX_AGE,
    JWT_ALGORITHM,
    JWT_SECRET,
    REFRESH_TOKEN_MAX_AGE,
    SUPABASE_KEY,
    SUPABASE_URL,
    ACCESS_TOKEN,
    REFRESH_TOKEN,
    SERVICES_LOG_LEVEL,
    DEV_MODE,
)
from ..models.token import TokenPayload
from ..models.users import UserLogin, UserRegister, UserRegisterResponse

logging.basicConfig(level=getattr(logging, SERVICES_LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



async def verify_token(request: Request) -> TokenPayload:
    access_token = request.cookies.get(ACCESS_TOKEN)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(
            access_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated",
        )
        return TokenPayload(**payload)
    except JWTError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def register(user: UserRegister) -> UserRegisterResponse:
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        return UserRegisterResponse(message="User created", user_id=response.user.id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")
    # Users should login by themselves after registration, because I hate them.


async def login(user: UserLogin) -> JSONResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        response = JSONResponse(
            content={
                ACCESS_TOKEN: res.session.access_token,
                REFRESH_TOKEN: res.session.refresh_token,
            }
        )
        set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed")


async def logout(payload: TokenPayload) -> JSONResponse:
    try:
        supabase.auth.sign_out()
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(ACCESS_TOKEN)
        response.delete_cookie(REFRESH_TOKEN)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Logout failed")


def give_account_info(payload: TokenPayload) -> TokenPayload:
    return payload


async def delete_all_cookies() -> JSONResponse:
    try:
        response = JSONResponse(content={"message": "Auth cookies successfully deleted"})
        response.delete_cookie(ACCESS_TOKEN)
        response.delete_cookie(REFRESH_TOKEN)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cookies cannot be deleted")


def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str):
    response.set_cookie(
        key=ACCESS_TOKEN,
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=not(DEV_MODE),
        max_age=ACCESS_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_MAX_AGE),
    )
    response.set_cookie(
        key=REFRESH_TOKEN,
        value=refresh_token,
        httponly=True,
        samesite="Strict",
        secure=not(DEV_MODE), 
        max_age=REFRESH_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_MAX_AGE),
    )
    return response
