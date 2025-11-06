from __future__ import annotations

from typing import Dict, List
from dataclasses import dataclass

from app.schemas.poi import POI


@dataclass
class InMemoryStore:
    poi_by_id: Dict[int, POI]

    @classmethod
    def create(cls) -> "InMemoryStore":
        return cls(poi_by_id={})

    def upsert_many(self, pois: List[POI]) -> None:
        for poi in pois:
            self.poi_by_id[poi.id] = poi

    def list_all(self) -> List[POI]:
        return list(self.poi_by_id.values())


