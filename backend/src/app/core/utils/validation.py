from app.api.routes.v1.schemas.response.validation import DocumentValidationResponse
from app.core.dao import Validation


def get_validation_schema(validation: Validation) -> DocumentValidationResponse:
    return DocumentValidationResponse(
        id=validation.id,
        errors = validation.errors
    )
