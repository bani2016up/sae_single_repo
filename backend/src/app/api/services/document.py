from collections.abc import Iterable
from typing import Optional
from app.core.dao import DocumentDAO, Document
from app.core.types import AsyncSession, idType, EXCEPTED_FILE_EXTENSIONS

from app.api.routes.v1.schemas.response.document import DocumentResponse, DocumentExtendedResponse
from app.api.routes.v1.schemas.request.document import CreateDocumentRequest, DocumentTitleUpdateRequest, DocumentTokenDeleteRequest, DocumentTokenInsertRequest
from fastapi import HTTPException, status

from fastapi import UploadFile

async def create_document(internal_user_id: idType, item: CreateDocumentRequest, sess: AsyncSession) -> DocumentResponse:
    """
    Create a new document for a specified user.

    Parameters:
    internal_user_id (idType): The ID of the user creating the document.
    item (CreateDocumentRequest): The request object containing the document details.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    DocumentResponse: The response object containing the created document's details.
    """
    instance: Document = Document(
        user_id = internal_user_id,
        title = item.title
    )
    document: Document = await DocumentDAO.create(instance, sess)
    return DocumentResponse(**document.__dict__)

async def get_documents(internal_user_id: idType, sess: AsyncSession) -> list[DocumentResponse]:
    """
    Retrieve all documents associated with a specified user.

    Parameters:
    internal_user_id (idType): The ID of the user whose documents are to be retrieved.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    list[DocumentResponse]: A list of response objects containing the details of each document.
    """
    documents: Iterable[Document] = await DocumentDAO.get_documents_by_user_id(internal_user_id, sess)
    return [DocumentResponse(**doc.__dict__) for doc in documents]

async def create_document_from_file(internal_user_id: idType, file: UploadFile, sess: AsyncSession) -> DocumentResponse:
    """
    Create a new document from an uploaded file for a specified user.

    Parameters:
    internal_user_id (idType): The ID of the user creating the document.
    file (UploadFile): The uploaded file object containing the document data.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    DocumentResponse: The response object containing the created document's details.

    Raises:
    HTTPException: If no file is provided or if the file extension is not supported.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No file provided."
        )
    if file.filename.split(".")[-1] not in EXCEPTED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt and .rtf files are supported."
        )
    content: bytes = await file.read()
    instance: Document = Document(
        user_id = internal_user_id,
        title = file.filename,
        content = content.decode()
    )
    document: Document = await DocumentDAO.create(instance, sess)
    return DocumentResponse(**document.__dict__)

async def delete_document(pk: idType, sess: AsyncSession) -> None:
    """
    Delete a document by its primary key.

    Parameters:
    pk (idType): The primary key of the document to be deleted.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    None: This function does not return a value.
    """
    await DocumentDAO.delete(pk, sess)

async def update_document_title(pk: idType, document_data: DocumentTitleUpdateRequest, sess: AsyncSession) -> DocumentResponse:
    """
    Update an existing document with new data.

    Parameters:
    pk (idType): The primary key of the document to be updated.
    document_data (DocumentUpdateRequest): The request object containing the updated document details.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    DocumentResponse: The response object containing the updated document's details.
    """
    document: Document = await DocumentDAO.update(pk, document_data.model_dump(), sess)
    return DocumentResponse(**document.__dict__)

async def get_document(pk: idType, sess: AsyncSession) -> DocumentExtendedResponse:
    """
    Retrieve a document by its primary key.

    Parameters:
    pk (idType): The primary key of the document to be retrieved.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    DocumentExtendedResponse: The response object containing the details of the retrieved document.

    Raises:
    HTTPException: If the document is not found.
    """
    document: Optional[Document] = await DocumentDAO.get(pk, sess)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return DocumentExtendedResponse(**document.__dict__)


async def insert_document_token(pk: idType, token: DocumentTokenInsertRequest, sess: AsyncSession) -> None:
    """
    Insert a token into a document at a specified position.

    This function retrieves a document by its primary key, inserts a token at the specified
    character position, and updates the document with the new content.

    Parameters:
    pk (idType): The primary key of the document to be updated.
    token (DocumentTokenInsertRequest): An object containing the token to be inserted and its position.
        It should have 'char' (the position to insert) and 'token' (the string to insert) attributes.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    None

    Raises:
    HTTPException: If the document with the given primary key is not found.
    """
    document: Optional[Document] = await DocumentDAO.get(pk, sess)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    content: str = document.content
    content_before: str = content[:token.char]
    content_after: str = content[token.char:]
    new_content: str = f"{content_before}{token.token}{content_after}"
    await DocumentDAO.update(pk, {"content": new_content}, sess)

async def delete_document_token(pk: idType, token: DocumentTokenDeleteRequest, sess: AsyncSession) -> None:
    """
    Delete a token from a document at a specified range.

    This function retrieves a document by its primary key, removes a token within the specified
    character range, and updates the document with the new content.

    Parameters:
    pk (idType): The primary key of the document to be updated.
    token (DocumentTokenDeleteRequest): An object containing the range of characters to be deleted.
        It should have 'char_start' (the starting position) and 'char_end' (the ending position) attributes.
    sess (AsyncSession): The asynchronous session for database operations.

    Returns:
    None

    Raises:
    HTTPException: If the document with the given primary key is not found.
    """
    document: Optional[Document] = await DocumentDAO.get(pk, sess)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    content: str = document.content
    content_before: str = content[:token.char_start]
    content_after: str = content[token.char_end:]
    new_content: str = f"{content_before}{content_after}"
    await DocumentDAO.update(pk, {"content": new_content}, sess)
