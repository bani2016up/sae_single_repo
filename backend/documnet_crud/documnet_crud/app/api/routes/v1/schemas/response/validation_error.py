from typing import Optional
from core.pydantic import BaseConfig


class ValidationError(BaseConfig):
    suggestion: str
    explanation: str
    wrong_fragment: str

    loc_index_ch_start: int
    loc_index_ch_end: int


class ValidationErrorResponse(BaseConfig):
    id: int
    is_resolved: bool

    error: Optional[ValidationError] = None
