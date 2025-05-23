from fastapi import FastAPI

from .middlewares import *  # contains ONLY middlewares
from .config.api import origins, methods, headers, allow_credentials, max_age
from .config.metadata import version
from ..api.routes import router as api_router

app = FastAPI(
    title="CRUD Backend API",
    version=version,
    contact={
        "name": "SAE",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=allow_credentials,
    max_age=max_age,
)
app.add_middleware(DynamicCORSMiddleware)
app.add_middleware(DatabaseAsyncSessionManager)
app.add_middleware(AutoRefreshTokenMiddleware)

app.include_router(api_router, prefix="/api", tags=["API"])
