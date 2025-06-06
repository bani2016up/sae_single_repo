
from .v1.endpoints.document import router as document_router
from .v1.endpoints.validation import router as validation_router
from ...auth.routers.routers import auth_router


from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(document_router)
router.include_router(validation_router)
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
