import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from supabase import Client, create_client

from ..config.cfg import (
    SUPABASE_KEY,
    SUPABASE_URL,
    ACCESS_TOKEN,
    REFRESH_TOKEN,
    AUTO_REFRESH_LOG_LEVEL,
)
from ..services.services import set_auth_cookies

# logging stays here, because I love it AND DON'T U DARE TAKE IT AWAY FROM ME!!!!
logging.basicConfig(level=getattr(logging, AUTO_REFRESH_LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class AutoRefreshTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get(ACCESS_TOKEN)
        refresh_token = request.cookies.get(REFRESH_TOKEN)

        if not access_token and not refresh_token:
            return await self.handle_no_tokens(request, call_next)

        if not access_token and refresh_token:
            return await self.handle_only_refresh_token(
                request, call_next, refresh_token
            )

        if access_token and not refresh_token:
            return await self.handle_only_access_token(request, call_next)

        return await call_next(request)

    async def handle_no_tokens(self, request: Request, call_next):
        logger.info(
            "No access or refresh token found, proceeding without authentication"
        )
        return await call_next(request)

    async def handle_only_refresh_token(
        self, request: Request, call_next, refresh_token: str
    ):
        logger.info("No access token found, proceeding update with refresh token")
        try:
            res = supabase.auth.refresh_session(refresh_token)
            logger.info("Token refreshed successfully")
            response = await call_next(request)
            set_auth_cookies(
                response,
                res.session.access_token,
                res.session.refresh_token,
            )
            return response
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Failed to refresh token"},
            )

    async def handle_only_access_token(self, request: Request, call_next):
        logger.info("No refresh token found, access token found. How the fu-")
        return await call_next(request)
