
from typing import Literal
from app.core.pydantic import BaseConfig
from .validation_error import ValidationErrorResponse


class DocumentValidationResponse(BaseConfig):
    id: int
    status: Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]


class DocumentValidationErrorsResponse(BaseConfig):
    errors: list[ValidationErrorResponse]
