from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from app.models.movie import PlatformEnum


class MovieIn(BaseModel):
    title: str
    rating: float
    year: int
    duration_minutes: int
    metascore: Optional[int] = None
    actors: List[str]
    detail_url: HttpUrl
    external_id: str
    platform: PlatformEnum
