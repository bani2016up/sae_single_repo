"""
This module defines interfaces for AI-based fact-checking services and vector storage backends.

Interfaces:
    - ``DeviceAwareModel``: Abstract base class for device-aware models.
    - ``FactCheckerInterface``: Interface for AI-based fact-checking services.
    - ``VectorStorageInterface``: Interface for vector storage backends.
"""

import functools

from abc import ABC, abstractmethod, ABCMeta
from typing import List, Dict, Self

from .response import SuggestionResponse
from .typing import DeviceType, PromptType, DocumentMetadataType

__all__ = (
    "DeviceAwareModel",
    "FactCheckerInterface",
    "VectorStorageInterface",
    "PromptInterface",
    "LLMInterface"
)


class _CatchKIMeta(ABCMeta):
    @staticmethod
    def _catch_keyboard_interrupt(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print(f"Interrupted in {func.__qualname__}")

        return wrapper

    @staticmethod
    def _catch_keyboard_interrupt_classmethod(func):
        @functools.wraps(func)
        def wrapper(cls, *args, **kwargs):
            try:
                return func(cls, *args, **kwargs)
            except KeyboardInterrupt:
                print(f"Interrupted in {func.__qualname__}")

        return wrapper

    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_val in list(namespace.items()):
            if attr_name.startswith("__"):
                continue

            if isinstance(attr_val, staticmethod):
                original_func = attr_val.__func__
                wrapped = mcs._catch_keyboard_interrupt(original_func)
                namespace[attr_name] = staticmethod(wrapped)

            elif isinstance(attr_val, classmethod):
                original_func = attr_val.__func__
                wrapped = mcs._catch_keyboard_interrupt_classmethod(original_func)
                namespace[attr_name] = classmethod(wrapped)

            elif callable(attr_val):
                namespace[attr_name] = mcs._catch_keyboard_interrupt(attr_val)

        if "__call__" in namespace and "forward" not in namespace:
            # usually the other way round, but I'm too lazy to redo it
            namespace["forward"] = namespace["__call__"]

        return super().__new__(mcs, name, bases, namespace)


class DeviceAwareModel(ABC, metaclass=_CatchKIMeta):
    """
    Abstract base class for all device-aware models.

    Defines a common interface for managing device placement.
    """

    def __init__(self, *, device: DeviceType = "cuda"):
        """
        Initializes the model on the specified device.

        Parameters:
            device (Literal["cpu", "cuda"]): Target device for model operations.
        """
        self._device = device

    @abstractmethod
    def to(self, device: DeviceType) -> Self:
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

    @property
    def device(self) -> DeviceType:
        """
        Returns the current device of the model.

        Returns:
            Literal["cpu", "cuda"]: The current device.
        """
        return self._device


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
    def add_document(
        self,
        index: int,
        text: str,
        metadata: DocumentMetadataType
    ) -> None:
        """
        Store a single document or fact vector in the index.

        Args:
            index (int): The unique identifier for the document.
            text (str): The raw text of the document.
            metadata (Dict[str, Any]): Any associated metadata for filtering or display.
        """
        ...

    @abstractmethod
    def add_documents(
        self,
        ids: List[int],
        texts: List[str],
        metadata: List[DocumentMetadataType]
    ) -> None:
        """
        Store multiple documents or fact vectors in bulk.

        Args:
            ids (List[int]): Unique identifiers for each document.
            texts (List[str]): The raw text for each document.
            metadata (List[Dict[str, Any]]): Metadata dicts corresponding to each document.
        """
        ...

    @abstractmethod
    def search(
        self,
        text: str,
        *,
        k: int = 5,
        threshold: float = 1.0,
        ner: List[str] = None
    ) -> List[DocumentMetadataType]:
        """
        Perform a semantic similarity search for the given query.

        Args:
            text (str): The query text to search for.
            k (int, optional): The number of nearest neighbors to return.
            threshold (float, optional): The minimum similarity score for results.
            ner (list[str], optional): Named entities to filter results.
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


class PromptInterface(ABC):
    @abstractmethod
    def __call__(self, **kwargs) -> PromptType:
        ...


class LLMInterface(DeviceAwareModel):
    """
    Abstract base class for LLM (Large Language Model) interfaces.
    This class defines the interface for LLMs, including methods for
    generating text and managing device placement.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs) -> str:
        """
        Generates text based on the provided input arguments.

        Args:
            *args: Positional arguments for the model.
            **kwargs: Keyword arguments for the model.

        Returns:
            str: The generated text.
        """
        ...
