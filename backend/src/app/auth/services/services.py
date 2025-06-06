import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from jose import JWTError, ExpiredSignatureError, jwt
from supabase import Client, create_client
from app.core.database.dao import UserDAO, User
from app.core.database.connection import AsyncSession


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
from ..models.credentials import CredentialsResponse
from ..models.users import (
    UserLogin,
    UserRegister,
    UserRegisterResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    AuthTokens,
    UserCredentialsChangeRequest,
    UserCredentialsChangeResponse,
)

logging.basicConfig(level=getattr(logging, SERVICES_LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def verify_token(request: Request) -> TokenPayload:
    access_token = request.cookies.get(ACCESS_TOKEN)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from e


async def register(user: UserRegister, sess: AsyncSession) -> UserRegisterResponse:
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        await UserDAO.create(User(
            external_id=response.user.id,
            username=user.email,
            email=user.email
        ), sess)
        return UserRegisterResponse(message="User created", user_id=response.user.id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed"
        ) from e
    # Users should login by themselves after registration, because I hate them.


async def login(user: UserLogin) -> JSONResponse:
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        response = JSONResponse(content={"message": "Logged in"})
        set_auth_cookies(response, res.session.access_token, res.session.refresh_token)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Login failed"
        )


async def logout(payload: TokenPayload) -> JSONResponse:
    try:
        supabase.auth.sign_out()
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(ACCESS_TOKEN)
        response.delete_cookie(REFRESH_TOKEN)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Logout failed"
        )

async def delete_all_cookies() -> JSONResponse:
    try:
        response = JSONResponse(
            content={"message": "Auth cookies successfully deleted"}
        )
        response.delete_cookie(ACCESS_TOKEN)
        response.delete_cookie(REFRESH_TOKEN)
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cookies cannot be deleted"
        )


def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str):
    response.set_cookie(
        key=ACCESS_TOKEN,
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=not (DEV_MODE),
        max_age=ACCESS_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_MAX_AGE),
    )
    response.set_cookie(
        key=REFRESH_TOKEN,
        value=refresh_token,
        httponly=True,
        samesite="Strict",
        secure=not (DEV_MODE),
        max_age=REFRESH_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_MAX_AGE),
    )
    return response


async def send_password_reset(user: PasswordResetRequest) -> PasswordResetResponse:
    try:
        supabase.auth.reset_password_for_email(
            user.email,
            {
                "redirect_to": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                # CHANGE IT TO ACTUAL LINK AFTER FRONTEND DID IT JOB
            },
        )
        return PasswordResetResponse(
            email=user.email,
            message="A password reset link has been sent to your email.",
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sending email with password reset failed",
        )


async def login_with_password_reset(tokens: AuthTokens) -> TokenPayload:
    try:
        response = JSONResponse(content={"message": "Logged in"})

        set_auth_cookies(response, tokens.access_token, tokens.refresh_token)
        supabase.auth.set_session(tokens.access_token, tokens.refresh_token)
        supabase.auth.refresh_session()
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Logout failed"
        )


async def change_password(
    payload: TokenPayload, credentials: UserCredentialsChangeRequest
) -> CredentialsResponse:
    try:
        response = supabase.auth.update_user({"password": credentials.new_password})
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def change_email(
    payload: TokenPayload, credentials: UserCredentialsChangeRequest
) -> CredentialsResponse:
    try:
        response = supabase.auth.update_user({"email": credentials.new_email})
        return response
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
