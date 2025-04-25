

import datetime
from app.core.pydantic import BaseConfig


class DocumentResponse(BaseConfig):
    id: int
    title: str
    was_created: datetime.datetime

class DocumentExtendedResponse(DocumentResponse):
    content: str
