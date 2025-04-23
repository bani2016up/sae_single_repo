import faiss
import numpy as np
import pickle

from typing import Any, Callable, Dict, List

from .interfaces import VectorStorageInterface


class VectorStorage(VectorStorageInterface):
    def __init__(
        self,
        dim: int,
        index_factory: str = "IVF100,Flat",
        embedder: Callable[[str], np.ndarray] = None
    ):
        self.dim = dim
        self.index_factory = index_factory
        self.embedder = embedder
        self.index = faiss.index_factory(self.dim, self.index_factory)
        self._metadata: Dict[int, Dict[str, Any]] = {}

    def train(self, vectors: np.ndarray) -> None:
        if hasattr(self.index, 'is_trained') and not self.index.is_trained:
            self.index.train(vectors)

    def add_document(self, index: int, text: str, metadata: Dict[str, Any]) -> None:
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
        metadata: List[Dict[str, Any]],
        *,
        use_tqdm: bool = False
    ) -> None:
        if self.embedder is None:
            raise ValueError("Embedder function must be provided.")

        vectors = np.asarray([self.embedder(t) for t in texts], dtype="float32")
        self.train(vectors)

        np_ids = np.array(ids, dtype="int64")
        self.index.add_with_ids(vectors, np_ids)
        for idx, md in zip(ids, metadata):
            self._metadata[idx] = md

    def search(self, text: str, *, k: int = 2) -> List[Dict[str, Any]]:
        if self.embedder is None:
            raise ValueError("Embedder function must be provided.")
        query_vec = np.asarray([self.embedder(text)], dtype="float32")
        distances, ids = self.index.search(query_vec, k)
        results: List[Dict[str, Any]] = []

        for dist, idx in zip(distances[0], ids[0]):
            if idx == -1:
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
        faiss_ids = np.array(document_ids, dtype="int64")
        self.index.remove_ids(faiss_ids)
        for doc_id in document_ids:
            self._metadata.pop(doc_id, None)

    def delete_document(self, document_id: int) -> None:
        self.delete_documents([document_id])

    def save(self, filepath: str) -> None:
        faiss.write_index(self.index, f"{filepath}.index")
        with open(f"{filepath}.pkl", "wb") as file:
            pickle.dump(self._metadata, file)

    def load(self, filepath: str) -> None:
        self.index = faiss.read_index(f"{filepath}.index")
        with open(f"{filepath}.pkl", "rb") as file:
            self._metadata = pickle.load(file)
           