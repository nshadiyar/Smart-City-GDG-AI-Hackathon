from typing import List, Tuple, Dict
import numpy as np

try:
    import faiss  # type: ignore
except Exception:  # pragma: no cover
    faiss = None  # Allows running without faiss installed yet

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover
    SentenceTransformer = None  # Allows running without model initially

from ..schemas.models import POI


class EmbeddingBackend:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self._model_name = model_name
        self._model = None

    def ensure_loaded(self) -> None:
        if self._model is None and SentenceTransformer is not None:
            self._model = SentenceTransformer(self._model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        if SentenceTransformer is None:
            # Fallback: simple hashing-based embedding for demo when deps unavailable
            rng = np.random.default_rng(42)
            return rng.random((len(texts), 384), dtype=np.float32)
        self.ensure_loaded()
        assert self._model is not None
        vectors = self._model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return vectors.astype(np.float32)


class FAISSIndex:
    def __init__(self, dim: int) -> None:
        self.dim = dim
        self.index = None
        self.id_map: List[int] = []

    def build(self, embeddings: np.ndarray, ids: List[int]) -> None:
        if faiss is None:
            self.index = None
            self.id_map = ids
            self._fallback_matrix = embeddings  # type: ignore[attr-defined]
            return
        self.index = faiss.IndexFlatIP(self.dim)
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)
        self.id_map = ids

    def search(self, query_vectors: np.ndarray, top_k: int) -> List[List[Tuple[int, float]]]:
        if self.index is None:
            # Fallback brute-force search
            from numpy.linalg import norm
            q = query_vectors
            D: List[List[Tuple[int, float]]] = []
            A = getattr(self, "_fallback_matrix")
            # cosine similarity
            A_norm = A / (norm(A, axis=1, keepdims=True) + 1e-9)
            q_norm = q / (norm(q, axis=1, keepdims=True) + 1e-9)
            sims = q_norm @ A_norm.T
            for row in sims:
                idxs = np.argsort(-row)[:top_k]
                D.append([(self.id_map[int(i)], float(row[int(i)])) for i in idxs])
            return D
        # FAISS path
        import faiss as _faiss  # local alias
        _faiss.normalize_L2(query_vectors)
        scores, inds = self.index.search(query_vectors, top_k)
        results: List[List[Tuple[int, float]]] = []
        for row_scores, row_inds in zip(scores, inds):
            items: List[Tuple[int, float]] = []
            for j in range(len(row_inds)):
                idx = int(row_inds[j])
                if idx < 0 or idx >= len(self.id_map):
                    continue
                items.append((self.id_map[idx], float(row_scores[j])))
            results.append(items)
        return results


class RAGEngine:
    def __init__(self) -> None:
        self.embedder = EmbeddingBackend()
        self.index: FAISSIndex | None = None
        self._id_to_doc: Dict[int, str] = {}

    def rebuild(self, pois: List[POI]) -> None:
        texts = [f"{p.name}. {p.desc}. tags: {,
