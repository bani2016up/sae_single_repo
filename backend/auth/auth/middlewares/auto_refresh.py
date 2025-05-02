from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.services import set_auth_cookies
from supabase import create_client, Client
from ..config.cfg import SUPABASE_KEY, SUPABASE_URL
import logging

# logging stays here, because I love it AND DON'T U DARE TAKE IT AWAY FROM ME!!!!
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class AutoRefreshTokenMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if not access_token and not refresh_token:
            logger.info(
                "No access and refresh token found, proceeding without authentication"
            )
            return await call_next(request)
        if not access_token and refresh_token:
            logger.info("No access token found, proceeding update with refresh token")
            try:
                res = supabase.auth.refresh_session(refresh_token)
                logger.info("Token refreshed successfully")
                response = await call_next(request)
                set_auth_cookies(
                    response, res.session.access_token, res.session.refresh_token
                )
                return response
            except Exception as e:
                logger.error(f"Failed to refresh token: {str(e)}")
                return JSONResponse(
                    status_code=401,
                    content={"detail": f"Failed to refresh token: {str(e)}"},
                )
        if access_token and not refresh_token:
            logger.info("No refresh token found, access token found. How the fu-")
            return await call_next(request)

        return await call_next(request)
