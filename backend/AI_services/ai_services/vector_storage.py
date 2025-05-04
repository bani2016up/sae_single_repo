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
        embedder (SentenceTransformer): A function to convert text to vectors.
        index (faiss.Index): The FAISS index for vector storage.
    """

    def __init__(
        self,
        dim: int,
        embedder: Callable[..., Union[torch.Tensor, np.ndarray]] = None
    ):
        """
        Initialize the VectorStorage with the specified parameters.
        Args:
            dim (int): The dimension of the vectors.
            embedder (Callable[[str], np.ndarray]): A function to convert text to vectors.
        """
        self.dim: int = dim
        self.embedder: Callable[..., Union[torch.Tensor, np.ndarray]] = embedder
        self.index = faiss.IndexFlatIP(self.dim)
        self._metadata: Dict[int, Dict[str, Any]] = {}
        self._id_to_offset: Dict[int, int] = {}
        self._offset_to_id: List[int] = []

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
        vec = self.embedder(text)
        vec /= np.linalg.norm(vec)
        arr = np.asarray([vec], dtype="float32")

        self.index.add(arr)
        self._id_to_offset[index] = len(self._offset_to_id)
        self._offset_to_id.append(index)
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
        vectors = np.asarray(
            [
                self.embedder(t, show_progress_bar=False) for t in tqdm(texts)
            ], dtype="float32"
        )
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        self.index.add(vectors)

        for idx in ids:
            self._id_to_offset[idx] = len(self._offset_to_id)
            self._offset_to_id.append(idx)

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
        query_vec = self.embedder(text, show_progress_bar=False)
        query_vec /= np.linalg.norm(query_vec)  # L2 normalization
        query_vec = np.asarray([query_vec], dtype="float32")

        distances, ids = self.index.search(query_vec, k)
        results: List[Dict[str, Any]] = []

        for dist, pos in zip(distances[0], ids[0]):
            if pos == -1 or dist > threshold:
                continue
            doc_id = self._offset_to_id[pos]
            results.append(
                {
                    "id": int(doc_id),
                    "score": float(dist),
                    "metadata": self._metadata.get(int(doc_id))
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
