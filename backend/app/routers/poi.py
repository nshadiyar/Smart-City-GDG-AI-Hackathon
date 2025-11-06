from typing import List
from fastapi import APIRouter

from app.schemas.poi import POI, ImportPOIRequest
from app.services.store import InMemoryStore
from app.services.recommend import RagRecommender


router = APIRouter()

store = InMemoryStore.create()
recommender = RagRecommender(store)


@router.get("/poi", response_model=List[POI])
async def list_poi() -> List[POI]:
    return store.list_all()


@router.post("/poi/import")
async def import_poi(payload: List[POI]) -> dict:
    store.upsert_many(payload)
    recommender.index_all()
    return {"imported": len(payload)}


