"""
This module defines the data models used for the response of the AI service.
It includes the following components:
1. ``ErrorPosition``: Represents the position of an error in the text.
2. ``SuggestionResponse``: Represents the result of evaluating a single factual assertion.
"""
from pydantic import BaseModel

__all__ = (
    "SuggestionResponse",
    "ErrorPosition"
)


class ErrorPosition(BaseModel):
    """
    Represents the position of an error in the text.

    Attributes:
        start (int): The starting index of the error in the text.
        end (int): The ending index of the error in the text.
        in_original (bool): Indicates if the position is in the original text.
    """
    start: int
    end: int
    in_original: bool = False


class SuggestionResponse(BaseModel):
    """
    Represents the result of evaluating a single factual assertion.

    Attributes:
        fact (str): The original assertion extracted from the input text.
        is_correct (bool): Indicates whether the assertion matches the known facts.
        position (ErrorPosition): The position of the assertion in the text.
        explanation (str): A human-readable explanation of any discrepancy.
    """
    fact: str
    position: ErrorPosition
    is_correct: bool
    explanation: str
