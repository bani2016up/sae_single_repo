import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request
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
)
from ..models.token import TokenPayload
from ..models.users import UserLogin, UserRegister

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def verify_token(request: Request) -> TokenPayload:
    access_token = request.cookies.get("access_token")
    if not auth_cookies:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(
            access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated"
        )
        return TokenPayload(**payload)
    except JWTError as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail=f"Invalid token")


async def register(user: UserRegister):
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        return {"message": "User created", "user_id": response.user.id}
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Registration failed")
    # Users should login by themselves after registration, because I hate them.


async def login(user: UserLogin) -> JSONResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        response = JSONResponse(
            content={
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
            }
        )
        set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=401, detail=f"Login failed")


async def logout(payload: TokenPayload) -> JSONResponse:
    try:
        supabase.auth.sign_out()
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Logout failed")


def give_account_info(payload: TokenPayload) -> TokenPayload:
    return payload


async def delete_all_cookies() -> JSONResponse:
    try:
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Cookies cannot be deleted")


def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True,
        max_age=ACCESS_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_MAX_AGE),
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Strict",
        secure=True,
        max_age=REFRESH_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_MAX_AGE),
    )
    return response
