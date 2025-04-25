from fastapi import APIRouter, UploadFile, File, Request, Response, status
from typing import List
from app.core.types import AsyncSession, idType

from ..schemas.response.document import DocumentResponse, DocumentExtendedResponse
from app.api.services import document as document_service
from app.api.routes.v1.schemas.request.document import CreateDocumentRequest, DocumentUpdateRequest

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(request: Request, response: Response, schema: CreateDocumentRequest) -> DocumentResponse:
    """
    Create a new document for the authenticated user.

    Args:
        request (Request): The HTTP request object containing user and session information.
        response (Response): The HTTP response object to set the status code.
        schema (CreateDocumentRequest): The schema containing the document data to be created.

    Returns:
        DocumentResponse: The response model containing the details of the created document.
    """
    user_id: idType = request.state.user_id
    sess: AsyncSession = request.state.sess
    response.status_code = status.HTTP_201_CREATED
    return await document_service.create_document(user_id, schema, sess)

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(request: Request) -> List[DocumentResponse]:
    """
    Retrieve a list of documents for the authenticated user.

    Args:
        request (Request): The HTTP request object containing user and session information.

    Returns:
        List[DocumentResponse]: A list of response models containing the details of the documents.
    """
    user_id: idType = request.state.user_id
    sess: AsyncSession = request.state.sess
    return await document_service.get_documents(user_id, sess)

@router.post("/from-file", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document_from_file(request: Request, response: Response, file: UploadFile = File(...)) -> DocumentResponse:
    """
    Create a new document from an uploaded file for the authenticated user.

    Args:
        request (Request): The HTTP request object containing user and session information.
        response (Response): The HTTP response object to set the status code.
        file (UploadFile): The uploaded file to be used for creating the document.

    Returns:
        DocumentResponse: The response model containing the details of the created document.
    """
    user_id: idType = request.state.user_id
    sess: AsyncSession = request.state.sess
    response.status_code = status.HTTP_201_CREATED
    return await document_service.create_document_from_file(user_id, file, sess)

@router.delete("/{pk}", response_model=None)
async def delete_document(request: Request, response: Response, pk: idType) -> Response:
    """
    Delete a document by its primary key.

    Args:
        request (Request): The HTTP request object containing user and session information.
        response (Response): The HTTP response object to set the status code.
        pk (int): The primary key of the document to be deleted.

    Returns:
        Response: The HTTP response object with a status code indicating the result of the operation.
    """
    sess: AsyncSession = request.state.sess
    await document_service.delete_document(pk, sess)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response

@router.put("/{pk}", response_model=DocumentResponse)
async def update_document(request: Request, response: Response, pk: idType, schema: DocumentUpdateRequest) -> DocumentResponse:
    """
    Update an existing document by its primary key.

    Args:
        request (Request): The HTTP request object containing user and session information.
        response (Response): The HTTP response object to set the status code.
        pk (int): The primary key of the document to be updated.
        schema (DocumentUpdateRequest): The schema containing the updated document data.

    Returns:
        DocumentResponse: The response model containing the details of the updated document.
    """
    sess: AsyncSession = request.state.sess
    document: DocumentExtendedResponse = await document_service.get_document(pk, sess)
    if DocumentUpdateRequest(**document.model_dump()) == schema:
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return DocumentResponse(**document.model_dump())
    return await document_service.update_document(pk, schema, sess)

@router.get("/{pk}", response_model=DocumentExtendedResponse)
async def get_document(request: Request, pk: idType) -> DocumentExtendedResponse:
    """
    Retrieve a document by its primary key.

    Args:
        request (Request): The HTTP request object containing user and session information.
        pk (int): The primary key of the document to be retrieved.

    Returns:
        DocumentExtendedResponse: The response model containing the details of the retrieved document.
    """
    sess: AsyncSession = request.state.sess
    return await document_service.get_document(pk, sess)
