from datetime import datetime
from pydantic import BaseModel, ConfigDict

class FavoriteMovieResponse(BaseModel):
    movie_id: int
    title: str
    genres: str | None = None
    poster_url: str | None = None
    overview: str | None = None

    model_config = ConfigDict(from_attributes=True)
    
class FavoriteResponse(BaseModel):
    id: int
    movie: FavoriteMovieResponse
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)