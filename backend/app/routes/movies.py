from fastapi import APIRouter,Query,HTTPException,Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.movie_service import (get_all_movies,get_movie_by_id)
from app.schemas.movie import (MovieResponse,MovieListResponse)

router=APIRouter(prefix='/api/movies',tags=['Movies'])

@router.get("/get_movies", response_model=MovieListResponse)
def get_movies(
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    search: str | None = Query(default=None),
    genre: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_all_movies(
        db=db,
        limit=limit,
        skip=skip,
        search=search,
        genre=genre
    )
    
#Get movie by id
@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = get_movie_by_id(db, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie