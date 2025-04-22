"""
    This module defines the ModelResponse class, which represents the result of evaluating a single factual assertion.
    It includes the following components:
    1. ``ModelResponse``: A dataclass that encapsulates the result of evaluating a factual assertion.
"""

from dataclasses import dataclass
from typing import Any, Dict

__all__ = (
    "ModelResponse",
)


@dataclass(repr=True, frozen=True, kw_only=True)
class ModelResponse(object):
    """
    Represents the result of evaluating a single factual assertion.

    Attributes:
        fact (str): The original assertion extracted from the input text.
        is_correct (bool): Indicates whether the assertion matches the known facts.
        explanation (str): A human-readable explanation of any discrepancy.
    """
    fact: str
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
            "explanation": self.explanation
        }
