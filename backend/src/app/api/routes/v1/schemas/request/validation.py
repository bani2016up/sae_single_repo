from app.core.pydantic import BaseConfig
from app.core.types import idType

class StartValidationRequest(BaseConfig):
    document_id: idType
