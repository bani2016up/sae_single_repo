
from app.core.pydantic import BaseConfig
from .validation_error import ValidationErrorResponse


class DocumentValidationResponse(BaseConfig):
    id: int
    validated: bool
    is_valid: bool


class DocumentValidationErrorsResponse(BaseConfig):
    errors: list[ValidationErrorResponse]
