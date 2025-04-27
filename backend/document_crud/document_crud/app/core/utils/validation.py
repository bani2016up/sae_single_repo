from app.api.routes.v1.schemas.response.validation import DocumentValidationResponse
from app.core.dao import Validation


def get_validation_schema(validation: Validation) -> DocumentValidationResponse:
    return DocumentValidationResponse(
        id=validation.id,
        validated=validation.validated,
        is_valid=validation.is_valid,
    )
