"""
    This module defines the ModelResponse class, which represents the result of evaluating a single factual assertion.
    It includes the following components:
    1. ``ModelResponse``: A dataclass that encapsulates the result of evaluating a factual assertion.
    2. ``ErrorPosition``: A dataclass that represents the position of an error in the text.
"""
from dataclasses import dataclass
from typing import Any, Dict

__all__ = (
    "SuggestionResponse",
    "ErrorPosition"
)


@dataclass(repr=True, frozen=True, kw_only=True)
class ErrorPosition(object):
    """
    Represents the position of an error in the text.
    """
    start: int
    end: int
    in_original: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error position to a dictionary.

        Returns:
            Dict[str, Any]: A dict with keys ``start``, ``end``, and ``in_original``.
        """
        return {
            "start": self.start,
            "end": self.end,
            "in_original": self.in_original,
        }


@dataclass(repr=True, frozen=True, kw_only=True)
class SuggestionResponse(object):
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.

        Returns:
            Dict[str, Any]: A dict with keys ``fact``, ``is_correct``, and ``explanation``.
        """
        return {
            "fact": self.fact,
            "is_correct": self.is_correct,
            "explanation": self.explanation,
            "position": self.position.to_dict()
        }
