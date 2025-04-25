
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from pydantic import BaseModel
from ..schemas.response.document import DocumentResponse, DocumentExtendedResponse

router = APIRouter(prefix="/documents", tags=[""])


@router.post("/", response_model=DocumentResponse)
async def create_document(document: BaseModel) -> DocumentResponse:
    # Implement the logic to create a document
    pass

@router.get("/", response_model=List[DocumentResponse])
async def get_() -> List[DocumentResponse]:
    # Implement the logic to retrieve a list of
    pass

@router.post("/from-file", response_model=DocumentResponse)
async def create_document_from_file(file: UploadFile = File(...)) -> DocumentResponse:
    # Implement the logic to create a document from a file
    pass

@router.delete("/{pk}", response_model=None)
async def delete_document(pk: int) -> None:
    # Implement the logic to delete a document
    pass

@router.put("/{pk}", response_model=DocumentResponse)
async def update_document(pk: int, document: BaseModel) -> DocumentResponse:
    # Implement the logic to update a document
    pass

@router.get("/{pk}", response_model=DocumentExtendedResponse)
async def get_document(pk: int) -> DocumentExtendedResponse:
    # Implement the logic to retrieve a single document
    pass
