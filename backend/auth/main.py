import uvicorn

from fastapi import APIRouter, FastAPI

from auth.config.cfg import HOST, PORT
from auth.middlewares.auto_refresh import AutoRefreshTokenMiddleware
from auth.routers.routers import auth_router as AuthRouter

app = FastAPI()

router = APIRouter()


api_version = "/v1"

routes = APIRouter(prefix="/api", redirect_slashes=False)

routes.include_router(AuthRouter, prefix=f"{api_version}/auth", tags=["auth"])

app.add_middleware(AutoRefreshTokenMiddleware)
app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
