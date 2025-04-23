
from fastapi import APIRouter, Depends, HTTPException
from core.db.session import AsyncSession

from fastapi.requests import Request
from core.permission import check_access_to_document

from ..schemas.response.project import ProjectResponse


router = APIRouter()


@router.get("/")
async def get_document_documents(request: Request):
    sess: AsyncSession = request.state.sess
    user_id: int = request.state.user_id
    return

@router.get("/{project_id}/documents/{document_id}")
async def get_document(request: Request, project_id: int):
    sess: AsyncSession = request.state.sess
    user_id: int = request.state.user_id
    check_access_to_document(
        project_id,
        user_id,
        sess
    )
    return


@router.get("/{project_id}/documents/{document_id}/abstract")
async def get_document(request: Request, project_id: int):
    sess: AsyncSession = request.state.sess
    user_id: int = request.state.user_id
    check_access_to_document(
        project_id,
        user_id,
        sess
    )
    return


@router.get("/{project_id}/documents/{document_id}/abstract")
async def get_document(request: Request, project_id: int):
    sess: AsyncSession = request.state.sess
    user_id: int = request.state.user_id
    check_access_to_document(
        project_id,
        user_id,
        sess
    )
    return
