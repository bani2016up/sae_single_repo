from app.core.pydantic import BaseConfig
from app.core.types import idType

class CreateValidationRequest(BaseConfig):
    document_id: idType
