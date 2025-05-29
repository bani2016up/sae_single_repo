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
                status = getattr(e, "status_code", 500)
                error_response = BaseResponse(status=status, message=str(e))
                response = JSONResponse(
                    status_code=status,
                    content=error_response.model_dump()
                )
            finally:
                await session.close()
            return response
