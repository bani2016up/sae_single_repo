"""
This module defines the data models used for the response of the AI service.
It includes the following components:
1. ``SuggestionPosition``: Represents the position of an error in the text.
2. ``SuggestionResponse``: Represents the result of evaluating a single factual assertion.
"""
from pydantic import BaseModel

__all__ = (
    "SuggestionResponse",
    "SuggestionPosition"
)


class SuggestionPosition(BaseModel):
    """
    Represents the position of an error in the text.

    Attributes:
        start_char_index (int): The starting index of the error in the text.
        end_char_index (int): The ending index of the error in the text.
        in_original (bool): Indicates if the position is in the original text.
    """
    start_char_index: int
    end_char_index: int
    in_original: bool = False


class SuggestionResponse(BaseModel):
    """
    Represents the result of evaluating a single factual assertion.

    Attributes:
        fact (str): The original assertion extracted from the input text.
        is_correct (bool): Indicates whether the assertion matches the known facts.
        position (SuggestionPosition): The position of the assertion in the text.
        explanation (str): A human-readable explanation of any discrepancy.
    """
    fact: str
    position: SuggestionPosition
    is_correct: bool
    explanation: str
