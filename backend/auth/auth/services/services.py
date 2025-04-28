from supabase import create_client, Client
from ..models.users import UserLogin, UserRegister
from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
from ..config.cfg import SUPABASE_KEY,SUPABASE_URL,JWT_SECRET,JWT_ALGORITHM

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


async def verify_token(request: Request):
    auth_cookies = request.cookies.get("access_token")
    if not auth_cookies:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = auth_cookies
    try:
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience="authenticated"
        )
        return payload  # This is a dict that includes sub (user id), email, etc.
    except JWTError as e:
        if "expired" in str(e).lower():
            raise HTTPException(status_code=401, detail="Token expired")
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


async def login(user: UserLogin):
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
        response.set_cookie(
            key="access_token",
            value=res.session.access_token,
            httponly=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=res.session.refresh_token,
            httponly=True,
            samesite="Strict",
            secure=True,
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed - Error: {e}")


async def logout(payload):
    try:
        supabase.auth.sign_out()
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def give_account_info(payload):
    return payload


async def delete_all_cookies():
    try:
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
