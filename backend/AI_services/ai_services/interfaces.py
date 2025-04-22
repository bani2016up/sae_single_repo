"""
This module defines interfaces for AI-based fact-checking services and vector storage backends.
It includes the following components:
1. ``AIServiceInterface``: An abstract base class defining the interface for AI-based fact-checking services.
2. ``VectorStorageInterface``: An abstract base class defining the interface for vector storage backends.
"""
from abc import ABC, abstractmethod
from typing import Any, List, Dict

from .response import ModelResponse

__all__ = (
    "FactCheckerInterface",
    "VectorStorageInterface"
)


class FactCheckerInterface(ABC):
    """
    Defines the interface for an AI-based fact-checking service.
    """

    @abstractmethod
    def evaluate_text(self, text: str, *, context: str = "") -> List[ModelResponse]:
        """
        Analyze the given text, split into assertions, and evaluate each.

        Args:
            text (str): The full text to evaluate.
            context (str, optional): Additional context or domain knowledge to guide evaluation.

        Returns:
            List[ModelResponse]: A list of ModelResponse instances for each assertion evaluated.
        """
        ...

    @abstractmethod
    def evaluate_sentence(self, sentences: str, *, context: str = "") -> ModelResponse:
        """
        Evaluate a single sentence or a small list of sentences.

        Args:
            sentences (str): One sentence to evaluate.
            context (str, optional): Additional context for the evaluation.

        Returns:
            ModelResponse: A ModelResponse instance with the evaluation result.
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
