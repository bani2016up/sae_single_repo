from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..config.api import origins as origins_cfg


class DynamicCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            response = await call_next(request)
        else:
            response = await call_next(request)
            origin = request.headers.get("origin")
            if origin in origins_cfg:
                response.headers["Access-Control-Allow-Origin"] = origin
        return response
