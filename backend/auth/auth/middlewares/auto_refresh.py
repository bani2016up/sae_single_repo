from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.services import verify_token, delete_all_cookies
from jose import ExpiredSignatureError
from supabase import create_client, Client
from ..config.cfg import SUPABASE_KEY,SUPABASE_URL

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class AutoRefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token:
            return await call_next(request)

        try:
            await verify_token(request)
            return await call_next(request)
        except HTTPException as e:
            if "expired" in str(e.detail).lower() and refresh_token:
                if not refresh_token:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "detail": "Access token expired, refresh token missing"
                        },
                    )

                try:
                    res = supabase.auth.refresh_session(refresh_token)
                    response = await call_next(request)
                    response.set_cookie(
                        "access_token",
                        res.session.access_token,
                        httponly=True,
                        samesite="Lax",
                    )
                    response.set_cookie(
                        "refresh_token",
                        res.session.refresh_token,
                        httponly=True,
                        samesite="Strict",
                        secure=True,
                    )
                    return response

                except Exception:
                    return JSONResponse(
                        status_code=401, content={"detail": "Failed to refresh token"}
                    )

        except Exception:

            return JSONResponse(
                status_code=401, content={"detail": "Invalid token, middleware"}
            )
