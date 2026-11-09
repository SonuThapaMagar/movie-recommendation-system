from fastapi import APIRouter,Query
from app.services.movie_service import get_all_movies

router=APIRouter(prefix='/api/movies',tags=['Movies'])

@router.get("/get_movies")
def get_movies(limit:int=Query(default=20,ge=1,le=100)): #ge=min :1, le=max=100
    movies=get_all_movies(limit)
    
    return {
        "count":len(movies),
        "movies":movies
    }