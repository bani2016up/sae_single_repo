from contextlib import suppress
from typing import Optional
from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth.services.services import verify_token, TokenPayload, JWTError
from app.core.dao import UserDAO, User
from app.core.database.connection import SessionLocal, AsyncSession
from ..pydantic import BaseResponse


class InternalUserIdSetter(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        sess: AsyncSession = request.state.sess
        if not sess:
            raise ValueError(
                "No database session found, one must first call database middleware."
            )
        internal_user_id = None
        with suppress(JWTError, HTTPException):
            payload: TokenPayload = await verify_token(request)
            external_user_id = payload.sub
            user: Optional[User] = await UserDAO.get_by_external_id(
                str(external_user_id), sess
            )
            internal_user_id = user.id if user else None
        request.state.internal_user_id = internal_user_id
        print(internal_user_id)

        return await call_next(request)
