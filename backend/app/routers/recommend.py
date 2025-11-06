from typing import List
from fastapi import APIRouter

from app.schemas.recommend import RecommendRequest, RecommendResponse
from app.schemas.poi import POI
from app.services.store import InMemoryStore
from app.services.recommend import RagRecommender


router = APIRouter()

store = InMemoryStore.create()
recommender = RagRecommender(store)


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest) -> RecommendResponse:
    # Ensure index reflects current POIs
    recommender.index_all()
    items = recommender.recommend(
        lat=req.lat,
        lon=req.lon,
        max_time_min=req.max_time_min,
        preferences=req.preferences,
        context=req.context,
        response_count=req.response_count,
    )
    return RecommendResponse(items=items)


