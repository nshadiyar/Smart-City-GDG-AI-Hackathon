from __future__ import annotations

from typing import List
import numpy as np

_model = None


def _lazy_load_model():
    global _model
    if _model is None:
        # Lightweight model for demo; downloads on first run
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    model = _lazy_load_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return np.asarray(vectors, dtype=np.float32)


