from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field

class RatingCreate(BaseModel):
    rating:float=Field(ge=1,le=10)
    
class RatingMovieResponse(BaseModel):
    movie_id:int
    title:str
    genres:str|None=None
    poster_url:str|None=None
    
    model_config=ConfigDict(from_attributes=True)
    
class UserRatingResponse(BaseModel):
    rating_id: int
    rating: float
    timestamp: int | None = None
    movie: RatingMovieResponse

    model_config = ConfigDict(from_attributes=True)