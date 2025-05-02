from supabase import create_client, Client
from ..models.users import UserLogin, UserRegister
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from ..config.cfg import SUPABASE_KEY,SUPABASE_URL,JWT_SECRET,JWT_ALGORITHM, ACCESS_TOKEN_MAX_AGE,REFRESH_TOKEN_MAX_AGE
from datetime import datetime, timedelta, timezone
from ..models.token import TokenPayload

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def verify_token(request: Request) -> TokenPayload:
    auth_cookies = request.cookies.get("access_token")
    if not auth_cookies:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_cookies
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated"
        )
        return TokenPayload(**payload)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token - Error: {e}")


async def register(user: UserRegister):
    try:
        response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )
        return {"message": "User created", "user_id": response.user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
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
        raise HTTPException(status_code=401, detail=f"Login failed - Error: {e}")


async def logout(payload: TokenPayload) -> JSONResponse:
    try:
        supabase.auth.sign_out()
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def give_account_info(payload: TokenPayload) -> TokenPayload:
    return payload


async def delete_all_cookies() -> JSONResponse:
    try:
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True,
        max_age=ACCESS_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_MAX_AGE)
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Strict",
        secure=True,
        max_age=REFRESH_TOKEN_MAX_AGE,
        expires=datetime.now(timezone.utc) + timedelta(seconds=REFRESH_TOKEN_MAX_AGE)
    )
    return response
