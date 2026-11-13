from pydantic import BaseModel, ConfigDict,Field 
#Pydantic helps FastAPI validate and serialize the data returned by API.

# Schema for a single movie
class MovieResponse(BaseModel):
    # Read movie_id from SQLAlchemy but return movieId to the frontend.
    movieId:int
    title:str
    genres:str=""
    tmdb_id: int | None = None
    poster_url: str | None = None
    overview: str | None = None
    rating: float | None = None
    release_date: str | None = None
    
    # Allows Pydantic to read SQLAlchemy model objects
    model_config = ConfigDict(from_attributes=True)
    
class MovieListResponse(BaseModel):
    count:int
    movies:list[MovieResponse]