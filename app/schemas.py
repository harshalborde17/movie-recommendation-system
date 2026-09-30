from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None
    director: Optional[str] = None
    cast: Optional[str] = None
    runtime: Optional[str] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
    source_url: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
