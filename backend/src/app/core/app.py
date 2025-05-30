from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middlewares import DatabaseAsyncSessionManager, AutoRefreshTokenMiddleware, InternalUserIdSetter, DynamicCORSMiddleware
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

# Middlewares are executed in reverse order of how they're added
# ----------------------------- Middlewares -----------------------------
# 5. CORS middleware (outermost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=allow_credentials,
    max_age=max_age,
)

# 4. Dynamic CORS middleware
app.add_middleware(DynamicCORSMiddleware)

# 3. Internal user ID setter
app.add_middleware(InternalUserIdSetter)

# 2. Auto refresh token middleware
app.add_middleware(AutoRefreshTokenMiddleware)

# 1. Database session middleware (innermost)
app.add_middleware(DatabaseAsyncSessionManager)

# ----------------------------- Middlewares -----------------------------

# Include API routes
app.include_router(api_router, prefix="/api", tags=["API"])
