"""
This module defines interfaces for AI-based fact-checking services and vector storage backends.

Interfaces:
    - ``DeviceAwareModel``: Abstract base class for device-aware models.
    - ``FactCheckerInterface``: Interface for AI-based fact-checking services.
    - ``VectorStorageInterface``: Interface for vector storage backends.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Literal

from .response import SuggestionResponse

__all__ = (
    "DeviceAwareModel",
    "FactCheckerInterface",
    "VectorStorageInterface"
)



class DeviceAwareModel(ABC):
    """
    Abstract base class for all device-aware models.

    Defines a common interface for managing device placement.
    """

    def __init__(self, *, device: Literal["cpu", "cuda"] = "cuda"):
        """
        Initializes the model on the specified device.

        Parameters:
            device (Literal["cpu", "cuda"]): Target device for model operations.
        """
        self.device = device

    @abstractmethod
    def to(self, device: Literal["cpu", "cuda"]) -> None:
        """
        Transfers the model to the specified device.

        Parameters:
            device (Literal["cpu", "cuda"]): A valid device string.

        Raises:
            ValueError: If the specified device is not supported.

        Examples:
            model.to("cuda")
        """
        ...


class FactCheckerInterface(DeviceAwareModel):
    """
    Defines the interface for an AI-based fact-checking service.
    """

    @abstractmethod
    def evaluate_text(self, text: str, *, context: str = "") -> List[SuggestionResponse]:
        """
        Analyze the given text, split into assertions, and evaluate each.

        Args:
            text (str): The full text to evaluate.
            context (str, optional): Additional context or domain knowledge to guide evaluation.

        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for each assertion evaluated.
        """
        ...

    @abstractmethod
    def evaluate_sentence(self, sentence: str, context: str = "") -> List[SuggestionResponse]:
        """
        Evaluate a single sentence.

        Args:
            sentence (str): One sentence to evaluate.
            context (str, optional): Additional context for the evaluation.

        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for the evaluated sentence.
        """
        ...


class VectorStorageInterface(ABC):
    """
    Defines the interface for a vector storage backend, used for semantic search.
    """

    @abstractmethod
    def add_document(self, index: int, text: str, metadata: Dict[str, Any]) -> None:
        """
        Store a single document or fact vector in the index.

        Args:
            index (int): The unique identifier for the document.
            text (str): The raw text of the document.
            metadata (Dict[str, Any]): Any associated metadata for filtering or display.
        """
        ...

    @abstractmethod
    def add_documents(self, ids: List[int], texts: List[str], metadata: List[Dict[str, Any]]) -> None:
        """
        Store multiple documents or fact vectors in bulk.

        Args:
            ids (List[int]): Unique identifiers for each document.
            texts (List[str]): The raw text for each document.
            metadata (List[Dict[str, Any]]): Metadata dicts corresponding to each document.
        """
        ...

    @abstractmethod
    def search(self, text: str, *, k: int = 2) -> List[Dict[str, Any]]:
        """
        Perform a semantic similarity search for the given query.

        Args:
            text (str): The query text to search for.
            k (int, optional): The number of nearest neighbors to return.

        Returns:
            List[Dict[str, Any]]: A list of search results, each containing
        """
        ...

    @abstractmethod
    def delete_document(self, document_id: int) -> None:
        """
        Remove a single document from the index.

        Args:
            document_id (int): The identifier of the document to delete.
        """
        ...

    @abstractmethod
    def delete_documents(self, document_ids: List[int]) -> None:
        """
        Remove multiple documents from the index.

        Args:
            document_ids (List[int]): Identifiers of the documents to delete.
        """
        ...

    @abstractmethod
    def load(self, filepath: str) -> None:
        """
        Load the index and metadata from persistent storage.

        Args:
            filepath (str): Path to the saved index file.
        """
        ...

    @abstractmethod
    def save(self, filepath: str) -> None:
        """
        Persist the current index and metadata to storage.

        Args:
            filepath (str): Destination path for saving the index.
        """
        ...
