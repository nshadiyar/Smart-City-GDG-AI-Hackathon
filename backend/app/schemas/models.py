from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field


class POI(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    tags: List[str] = Field(default_factory=list)
    desc: str = ""


class RecommendationRequest(BaseModel):
    lat: float
    lon: float
    max_time_min: int = 60
    preferences: List[str] = Field(default_factory=list)
    context: Dict[str, object] = Field(default_factory=dict)
    response_count: int = 3


class RecommendationItem(BaseModel):
    name: str
    distance_m: int
    why: str
    visit_min: int
    actions: str
    confidence: Literal["high", "medium", "low"]
    source: Literal["POI", "RAG", "RULES"] = "POI"


class RecommendationResponse(BaseModel):
    items: List[RecommendationItem]
