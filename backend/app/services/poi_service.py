from typing import Dict, List, Tuple
from .geo import haversine_meters
from ..schemas.models import POI


class POIStore:
    def __init__(self) -> None:
        self._id_to_poi: Dict[int, POI] = {}

    def all(self) -> List[POI]:
        return list(self._id_to_poi.values())

    def upsert_many(self, pois: List[POI]) -> None:
        for poi in pois:
            self._id_to_poi[poi.id] = poi

    def nearest_within(self, lat: float, lon: float, radius_m: float) -> List[Tuple[POI, float]]:
        user = (lat, lon)
        results: List[Tuple[POI, float]] = []
        for poi in self._id_to_poi.values():
            d = haversine_meters(user, (poi.lat, poi.lon))
            if d <= radius_m:
                results.append((poi, d))
        results.sort(key=lambda x: x[1])
        return results


poi_store = POIStore()
