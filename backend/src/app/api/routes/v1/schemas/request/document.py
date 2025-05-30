from app.core.pydantic import BaseConfig


class CreateDocumentRequest(BaseConfig):
    title: str


class DocumentTitleUpdateRequest(BaseConfig):
    title: str

class DocumentTokenInsertRequest(BaseConfig):
    char: int
    token: str


class DocumentTokenDeleteRequest(BaseConfig):
    char_start: int
    char_end: int
