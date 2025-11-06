from __future__ import annotations

from typing import List, Dict, Tuple
from math import radians, cos, sin, asin, sqrt

from app.schemas.poi import POI
from app.schemas.recommend import Recommendation
from app.services.store import InMemoryStore
from app.services.embeddings import embed_texts
from app.services.vector import FaissIndex
from app.services.llm import build_prompt, generate_with_mock


def haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius km
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c * 1000.0


class RagRecommender:
    def __init__(self, store: InMemoryStore):
        self.store = store
        self._vector_index: FaissIndex | None = None
        self._dim: int | None = None

    def index_all(self) -> None:
        pois = self.store.list_all()
        texts = [f"{p.name}. {p.desc or ''} Tags: {', '.join(p.tags)}" for p in pois]
        if not texts:
            self._vector_index = None
            return
        vectors = embed_texts(texts)
        self._dim = vectors.shape[1]
        index = FaissIndex(self._dim)
        index.add([p.id for p in pois], vectors)
        self._vector_index = index

    def nearby_pois(self, lat: float, lon: float, radius_m: float = 2000.0) -> List[Tuple[POI, float]]:
        res: List[Tuple[POI, float]] = []
        for poi in self.store.list_all():
            d = haversine_distance_m(lat, lon, poi.lat, poi.lon)
            if d <= radius_m:
                res.append((poi, d))
        res.sort(key=lambda x: x[1])
        return res

    def search_relevant(self, query: str, candidates: List[POI], top_k: int = 5) -> List[POI]:
        if not candidates:
            return []
        if self._vector_index is None:
            self.index_all()
        if self._vector_index is None:
            return candidates[:top_k]

        cand_texts = [f"{p.name}. {p.desc or ''} Tags: {', '.join(p.tags)}" for p in candidates]
        cand_vectors = embed_texts(cand_texts)
        # Build a temp index for candidates to rank by semantic similarity to the query
        query_vec = embed_texts([query])
        # Using inner product with normalized embeddings ≈ cosine
        index = FaissIndex(cand_vectors.shape[1])
        index.add([p.id for p in candidates], cand_vectors)
        results = index.search(query_vec, top_k)
        id_order = [pid for pid, _ in results[0]] if results else []
        id_to_poi = {p.id: p for p in candidates}
        ranked = [id_to_poi[i] for i in id_order if i in id_to_poi]
        # Fallback if FAISS returns nothing
        if not ranked:
            ranked = candidates[:top_k]
        return ranked

    def recommend(
        self,
        lat: float,
        lon: float,
        max_time_min: int,
        preferences: List[str],
        context: Dict[str, object],
        response_count: int,
    ) -> List[Recommendation]:
        nearby = self.nearby_pois(lat, lon)
        if not nearby:
            # No data; return mock generic
            llm_items = generate_with_mock("", response_count)
            return [
                Recommendation(
                    name=i["name"],
                    why=i["why"],
                    actions=i["actions"],
                    visit_min=int(i["visit_min"]),
                    confidence=i["confidence"],
                    distance_m=0,
                    source="RULE",
                )
                for i in llm_items
            ]

        candidate_pois = [p for p, _ in nearby]
        pref_text = ", ".join(preferences) if preferences else ""
        query = f"{pref_text} {context}".strip()
        top_pois = self.search_relevant(query, candidate_pois, top_k=max(5, response_count))

        context_items = []
        id_to_dist = {p.id: d for p, d in nearby}
        for p in top_pois:
            context_items.append(
                {
                    "name": p.name,
                    "desc": p.desc or "",
                    "distance_m": int(id_to_dist.get(p.id, 0)),
                    "tags": p.tags,
                }
            )

        prompt = build_prompt(lat, lon, max_time_min, preferences, context, context_items)
        llm_items = generate_with_mock(prompt, response_count)
        recs: List[Recommendation] = []
        for item in llm_items:
            # Try to map to nearest chosen POI for distance; else 0
            chosen = top_pois[0] if top_pois else None
            dist = int(id_to_dist.get(chosen.id, 0)) if chosen else 0
            recs.append(
                Recommendation(
                    name=item.get("name", chosen.name if chosen else "Рекомендация"),
                    why=item.get("why", "Рядом и подходит под запрос"),
                    actions=item.get("actions", ""),
                    visit_min=int(item.get("visit_min", max_time_min)),
                    confidence=item.get("confidence", "medium"),
                    distance_m=dist,
                    source="POI",
                )
            )

        return recs[:response_count]


