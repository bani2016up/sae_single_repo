from fastapi import APIRouter, Request, Response, status, HTTPException
from app.core.types import AsyncSession, idType
from ..schemas.request.validation import CreateValidationRequest
from ..schemas.response.validation import DocumentValidationErrorsResponse, DocumentValidationResponse
from app.api.services import validation as validation_service

router = APIRouter(prefix="/validation", tags=["Validation"])

@router.post("/", response_model=DocumentValidationResponse, status_code=status.HTTP_201_CREATED)
async def create_validation(request: Request, response: Response, item: CreateValidationRequest) -> DocumentValidationResponse:
    """
    Create a new validation entry for the authenticated user.

    Args:
        request (Request): The HTTP request object containing user and session information.
        response (Response): The HTTP response object to set the status code.
        item (CreateValidationRequest): The request model containing the validation details.

    Returns:
        DocumentValidationResponse: The response model containing the details of the created validation.
    """
    sess: AsyncSession = request.state.sess
    response.status_code = status.HTTP_201_CREATED
    return await validation_service.create_validation(item, sess)

@router.post("/{pk}/start", response_model=DocumentValidationResponse)
async def start_validation(request: Request, response: Response, pk: int) -> DocumentValidationResponse:
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
    return await validation_service.start_validation(pk, sess)

@router.put("/{pk}/reset", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def reset_validation(request: Request, response: Response, pk: idType) -> Response:
    """
    Reset the validation status for a specific validation entry.

    Args:
        request (Request): The HTTP request object containing session information.
        response (Response): The HTTP response object to set the status code.
        pk (idType): The primary key of the validation entry to reset.

    Returns:
        Response: An empty response with a 204 No Content status.
    """
    sess: AsyncSession = request.state.sess
    await validation_service.reset_validation(pk, sess)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

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
