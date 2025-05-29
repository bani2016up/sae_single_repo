from typing import Optional
from fastapi import HTTPException, status

from app.core.dao import ValidationDAO, ErrorDAO, DocumentDAO, Validation, Document
from app.api.routes.v1.schemas.request.validation import StartValidationRequest
from app.api.routes.v1.schemas.response.validation import (
    DocumentValidationResponse,
    DocumentValidationErrorsResponse,
)
from app.core.types import AsyncSession, idType
from app.core.utils.validation import get_validation_schema


async def start_validation(
    document_pk: idType, sess: AsyncSession
) -> DocumentValidationResponse:
    # validation: Optional[Validation] = await ValidationDAO.create(
    #     Validation(document_id=document_pk), sess
    # )
    # return get_validation_schema(validation)



async def reset_validation(pk: idType, sess: AsyncSession) -> None:
    """
    Resets the validation status of a document.

    Parameters:
    pk (idType): The primary key of the validation to reset.
    sess (AsyncSession): The database session used for the operation.

    Returns:
    None: This function does not return a value. It raises an HTTPException if the validation is not found.
    """
    validation: Optional[Validation] = await ValidationDAO.get(pk, sess)
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Validation not found"
        )

    validation.validated = False
    validation.is_valid = None
    await ErrorDAO.delete_where_validation_id(validation.id, sess)


async def get_validation(pk: idType, sess: AsyncSession) -> DocumentValidationResponse:
    """
    Retrieves the validation details for a given document.

    Parameters:
    pk (idType): The primary key of the validation to retrieve.
    sess (AsyncSession): The database session used for the operation.

    Returns:
    DocumentValidationResponse: The validation details of the document. Raises an HTTPException if the validation is not found.
    """
    validation: Optional[Validation] = await ValidationDAO.get(pk, sess)
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Validation not found"
        )
    return get_validation_schema(validation)


async def get_validation_errors(
    pk: idType, sess: AsyncSession
) -> DocumentValidationErrorsResponse:
    """
    Retrieves the validation errors for a given document.

    Parameters:
    pk (idType): The primary key of the validation to retrieve errors for.
    sess (AsyncSession): The database session used for the operation.

    Returns:
    DocumentValidationErrorsResponse: An object containing the validation errors of the document.
    Raises an HTTPException if the validation is not found.
    """
    validation: Optional[Validation] = await ValidationDAO.get(pk, sess)
    if not validation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Validation not found"
        )
    return DocumentValidationErrorsResponse(errors=validation.awaitable_attrs.errors)


async def create_validation(
    internal_user_id: idType, schema: StartValidationRequest, sess: AsyncSession
) -> DocumentValidationResponse:
    """
    Creates a new validation entry for a document.

    Parameters:
    internal_user_id (idType): The ID of the user creating the validation.
    schema (CreateValidationRequest): The request model containing the validation details.
    sess (AsyncSession): The database session used for the operation.

    Returns:
    DocumentValidationResponse: The response model containing the details of the created validation.
    Raises an HTTPException if the document is not found or if the validation cannot be created.
    """

    document: Optional[Document] = await DocumentDAO.get(schema.document_id, sess)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found"
        )

    validation = Validation(
        internal_user_id=internal_user_id,
        document_id=schema.document_id,
        validated=False,
        is_valid=None,
    )
    created_validation: Validation = await ValidationDAO.create(validation, sess)

    return get_validation_schema(created_validation)
