import uvicorn

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.config.cfg import HOST, PORT
from auth.middlewares.auto_refresh import AutoRefreshTokenMiddleware
from auth.routers.routers import auth_router as AuthRouter

app = FastAPI()

router = APIRouter()


api_version = "/v1"

routes = APIRouter(prefix="/api", redirect_slashes=False)

routes.include_router(AuthRouter, prefix=f"{api_version}/auth", tags=["auth"])

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    max_age=3600,
)

app.add_middleware(AutoRefreshTokenMiddleware)
app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
