from app.core.pydantic import BaseConfig


class CreateDocumentRequest(BaseConfig):
    title: str


class DocumentUpdateRequest(BaseConfig):
    title: str
