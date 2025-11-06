from __future__ import annotations

from typing import List, Tuple
import faiss  # type: ignore
import numpy as np


class FaissIndex:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.ids: List[int] = []

    def add(self, ids: List[int], vectors: np.ndarray) -> None:
        if vectors.dtype != np.float32:
            vectors = vectors.astype(np.float32)
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, query_vectors: np.ndarray, top_k: int) -> List[List[Tuple[int, float]]]:
        if query_vectors.dtype != np.float32:
            query_vectors = query_vectors.astype(np.float32)
        scores, idxs = self.index.search(query_vectors, top_k)
        results: List[List[Tuple[int, float]]] = []
        for i in range(len(query_vectors)):
            pairs: List[Tuple[int, float]] = []
            for j in range(idxs.shape[1]):
                if idxs[i, j] == -1:
                    continue
                poi_id = self.ids[idxs[i, j]]
                pairs.append((poi_id, float(scores[i, j])))
            results.append(pairs)
        return results


