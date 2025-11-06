from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    lat: float
    lon: float
    max_time_min: int = 60
    preferences: List[str] = Field(default_factory=list)
    context: Dict[str, object] = Field(default_factory=dict)
    response_count: int = 3


class Recommendation(BaseModel):
    name: str
    distance_m: int
    why: str
    visit_min: int
    actions: str
    confidence: Literal["high", "medium", "low"]
    source: Literal["POI", "LLM", "RULE"]


class RecommendResponse(BaseModel):
    items: List[Recommendation]


