import uvicorn
from fastapi import FastAPI, APIRouter
from auth.routers.routers import auth_router as AuthRouter
from auth.middlewares.auto_refresh import AutoRefreshTokenMiddleware
from auth.config.cfg import HOST,PORT

app = FastAPI()

router = APIRouter()


api_version = "/v1"

routes = APIRouter(prefix="/auth_api", redirect_slashes=False)

routes.include_router(AuthRouter, prefix=f"{api_version}/auth", tags=["users"])

app.add_middleware(AutoRefreshTokenMiddleware)
app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
