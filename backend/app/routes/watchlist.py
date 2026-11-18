from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.watchlist import WatchlistResponse
from app.schemas.response import ApiResponse
from app.services.watchlist_service import (
    add_to_watchlist,
    get_user_watchlist,
    remove_from_watchlist
)
from app.utils.response import success_response


router = APIRouter(prefix='/api/watchlist',tags=["Watchlist"])

@router.post("/{movie_id}",response_model=ApiResponse[WatchlistResponse],status_code=status.HTTP_201_CREATED)
def add_movie_to_watchlist(movie_id:int,request:Request,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    watchlist_item, error = add_to_watchlist(
        db,
        current_user.id,
        movie_id
    )
    
    if error == "Movie not found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )

    if error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error
        )

    return success_response(
        request,
        status.HTTP_201_CREATED,
        "Movie added to watchlist successfully",
        watchlist_item
    )
    
@router.get(
    "",
    response_model=ApiResponse[list[WatchlistResponse]]
)
def get_watchlist(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    watchlist = get_user_watchlist(db, current_user.id)

    return success_response(
        request,
        status.HTTP_200_OK,
        "Watchlist retrieved successfully",
        watchlist
    )
    
@router.delete(
    "/{movie_id}",
    response_model=ApiResponse[None]
)
def delete_from_watchlist(
    movie_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = remove_from_watchlist(
        db,
        current_user.id,
        movie_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found in watchlist"
        )

    return success_response(
        request,
        status.HTTP_200_OK,
        "Movie removed from watchlist successfully"
    )

