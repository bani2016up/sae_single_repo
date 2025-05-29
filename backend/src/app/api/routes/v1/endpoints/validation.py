from fastapi import APIRouter, Request, Response, status, HTTPException
from app.core.types import AsyncSession, idType
from ..schemas.request.validation import StartValidationRequest
from ..schemas.response.validation import DocumentValidationErrorsResponse, DocumentValidationResponse
from app.api.services import validation as validation_service

router = APIRouter(prefix="/validation", tags=["Validation"])


@router.post("/", response_model=DocumentValidationResponse)
async def start_validation(request: Request, schema: StartValidationRequest,  pk: int) -> DocumentValidationResponse:
    """
    Start the validation process for a specific validation entry.

    Args:
        request (Request): The HTTP request object containing session information.
        response (Response): The HTTP response object to set the status code.
        pk (int): The primary key of the validation entry to start.

    Returns:
        DocumentValidationResponse: The response model containing the details of the started validation.
    """
    sess: AsyncSession = request.state.sess
    return await validation_service.start_validation(schema, sess)


@router.get("/{pk}", response_model=DocumentValidationResponse)
async def get_validation(request: Request, pk: idType) -> DocumentValidationResponse:
    """
    Retrieve a specific validation entry by its primary key.

    Args:
        request (Request): The HTTP request object containing session information.
        pk (idType): The primary key of the validation entry to retrieve.

    Returns:
        DocumentValidationResponse: The response model containing the details of the validation.
    """
    sess: AsyncSession = request.state.sess
    return await validation_service.get_validation(pk, sess)

@router.get("/{pk}/errors", response_model=DocumentValidationErrorsResponse)
async def get_validation_errors(request: Request, pk: idType) -> DocumentValidationErrorsResponse:
    """
    Retrieve validation errors for a specific validation entry.

    Args:
        request (Request): The HTTP request object containing session information.
        pk (idType): The primary key of the validation entry to retrieve errors for.

    Returns:
        DocumentValidationErrorsResponse: The response model containing the validation errors.
    """
    sess: AsyncSession = request.state.sess
    return await validation_service.get_validation_errors(pk, sess)
