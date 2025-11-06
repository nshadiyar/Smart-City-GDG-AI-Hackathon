from typing import List, Optional
from pydantic import BaseModel, Field, RootModel


class POI(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    tags: List[str] = Field(default_factory=list)
    desc: Optional[str] = None


class ImportPOIRequest(RootModel[List[POI]]):
    root: List[POI]

    def to_list(self) -> List[POI]:
        return self.root


