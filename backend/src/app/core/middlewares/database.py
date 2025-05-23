from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database.connection import SessionLocal, AsyncSession
from ..pydantic import BaseResponse


class DatabaseAsyncSessionManager(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with SessionLocal() as session:
            session: AsyncSession
            request.state.sess = session
            try:
                response = await call_next(request)
                await session.commit()
            except Exception as e:
                await session.rollback()
                error_response = BaseResponse(status=500, message=str(e))
                response = JSONResponse(content=error_response.model_dump())
            return response
