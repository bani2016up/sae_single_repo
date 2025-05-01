"""
Vector Storage using FAISS
This module provides a class for managing vector storage using FAISS.
It includes methods for adding, searching, and deleting vectors,
as well as saving and loading the index to/from disk.
It also allows for the storage of associated metadata.
"""
import faiss
import torch
import numpy as np
import pickle

from typing import Any, Dict, List, Callable, Union
from tqdm.auto import tqdm

from .interfaces import VectorStorageInterface
from .typing import DocumentMetadataType

__all__ = (
    "VectorStorage",
)


class VectorStorage(VectorStorageInterface):
    """
    A class to manage vector storage using FAISS.
    This class provides methods to add, search, and delete vectors,
    as well as save and load the index to/from disk.
    It also allows for the storage of associated metadata.
    Attributes:
        dim (int): The dimension of the vectors.
        index_factory (str): The index factory string for FAISS.
        embedder (SentenceTransformer): A function to convert text to vectors.
        index (faiss.Index): The FAISS index for vector storage.
    """

    def __init__(
        self,
        dim: int,
        index_factory: str = "IVF100,Flat",
        embedder: Callable[..., Union[torch.Tensor, np.ndarray]] = None
    ):
        """
        Initialize the VectorStorage with the specified parameters.
        Args:
            dim (int): The dimension of the vectors.
            index_factory (str): The index factory string for FAISS.
            embedder (Callable[[str], np.ndarray]): A function to convert text to vectors.
        """
        self.dim: int = dim
        self.embedder: Callable[..., Union[torch.Tensor, np.ndarray]] = embedder
        # <class ‘faiss.swigfaiss.IndexIVFFlat’>, but if you explicitly specify the type
        # the IDE outputs a lot of warnings
        self.index = faiss.index_factory(self.dim, index_factory)
        self._metadata: Dict[int, DocumentMetadataType] = {}

    def train(self, vectors: np.ndarray) -> None:
        """
        Train the FAISS index with the provided vectors.

        Args:
            vectors (np.ndarray): The vectors to train the index with.
        """
        if hasattr(self.index, 'is_trained') and not self.index.is_trained:
            self.index.train(vectors)

    def add_document(self, index: int, text: str, metadata: DocumentMetadataType) -> None:
        """
        Add a single document to the vector storage.
        Args:
            index (int): The ID of the document.
            text (str): The text content of the document.
            metadata (Dict[str, Any]): Metadata associated with the document.
        Raises:
            ValueError: If the embedder function is not provided.
        """
        if self.embedder is None:
            raise ValueError("Embedder function must be provided.")
        vec = self.embedder(text)
        arr = np.asarray([vec], dtype="float32")

        self.train(arr)
        self.index.add_with_ids(arr, np.asarray([index], dtype='int64'))
        self._metadata[index] = metadata

    def add_documents(
        self,
        ids: List[int],
        texts: List[str],
        metadata: List[DocumentMetadataType]
    ) -> None:
        """
        Add multiple documents to the vector storage.
        Args:
            ids (List[int]): The IDs of the documents.
            texts (List[str]): The text content of the documents.
            metadata (List[Dict[str, Any]]): Metadata associated with the documents.
        Raises:
            ValueError: If the embedder function is not provided.
        """
        if self.embedder is None:
            raise ValueError("Embedder function must be provided.")

        vectors = np.asarray(
            [
                self.embedder(t, show_progress_bar=False) for t in tqdm(texts)
            ], dtype="float32"
        )
        self.train(vectors)

        np_ids = np.array(ids, dtype="int64")

        self.index.add_with_ids(vectors, np_ids)
        for idx, md in zip(ids, metadata):
            self._metadata[idx] = md

    def search(self, text: str, *, k: int = 5, threshold: float = 1.0) -> List[DocumentMetadataType]:
        """
        Search for the nearest neighbors of the given text in the vector storage.
        Args:
            text (str): The text to search for.
            k (int): The number of nearest neighbors to return.
            threshold (float): The distance threshold for filtering results.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing the ID, score,
                                  and metadata of the nearest neighbors.
        Raises:
            ValueError: If the embedder function is not provided.
        """
        if self.embedder is None:
            raise ValueError("Embedder function must be provided.")
        query_vec = np.asarray(
            [
                self.embedder(text, show_progress_bar=False)
            ], dtype="float32"
        )
        distances, ids = self.index.search(query_vec, k)
        results: List[Dict[str, Any]] = []

        for dist, idx in zip(distances[0], ids[0]):
            if idx == -1 or dist > threshold:
                continue
            results.append(
                {
                    "id": int(idx),
                    "score": float(dist),
                    "metadata": self._metadata.get(int(idx))
                }
            )
        return results

    def delete_documents(self, document_ids: List[int]) -> None:
        """
        Delete multiple documents from the vector storage.
        Args:
            document_ids (List[int]): The IDs of the documents to delete.
        """
        faiss_ids = np.array(document_ids, dtype="int64")
        self.index.remove_ids(faiss_ids)
        for doc_id in document_ids:
            self._metadata.pop(doc_id, None)

    def delete_document(self, document_id: int) -> None:
        """
        Delete a single document from the vector storage.
        Args:
            document_id (int): The ID of the document to delete.
        """
        self.delete_documents([document_id])

    def save(self, filepath: str) -> None:
        """
        Save the FAISS index and metadata to disk.
        Args:
            filepath (str): The base file path to save the index and metadata.
        """
        faiss.write_index(self.index, f"{filepath}.index")
        with open(f"{filepath}.pkl", "wb") as file:
            pickle.dump(self._metadata, file)

    def load(self, filepath: str) -> None:
        """
        Load the FAISS index and metadata from disk.
        Args:
            filepath (str): The base file path to load the index and metadata from.
        """
        self.index = faiss.read_index(f"{filepath}.index")
        with open(f"{filepath}.pkl", "rb") as file:
            self._metadata = pickle.load(file)
