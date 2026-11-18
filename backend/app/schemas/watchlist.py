from datetime import datetime
from pydantic import BaseModel,ConfigDict # allow pydantic to read value directly from sqlalchemy model oj

class WatchlistMovieResponse(BaseModel):
    movie_id:int
    title:str
    genres:str | None=None
    poster_url:str| None=None
    overview:str|None=None
    
    model_config=ConfigDict(from_attributes=True)
    
class WatchlistResponse(BaseModel):
    id:int
    movie:WatchlistMovieResponse
    created_at:datetime
    
    model_config = ConfigDict(from_attributes=True)