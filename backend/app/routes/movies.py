from fastapi import APIRouter,Query,HTTPException
from app.services.movie_service import (get_all_movies,get_movie_by_id)

router=APIRouter(prefix='/api/movies',tags=['Movies'])

@router.get("/get_movies")
def get_movies(limit:int=Query(default=20,ge=1,le=100)): #ge=min :1, le=max=100
    movies=get_all_movies(limit)
    
    return {
        "count":len(movies),
        "movies":movies
    }

#Get movie by id
@router.get("/{movie_id}")
def get_movie(movie_id:int):
    movie=get_movie_by_id(movie_id)
    if movie_id is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    return movie