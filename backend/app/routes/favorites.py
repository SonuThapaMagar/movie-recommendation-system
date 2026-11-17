from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.favorite import FavoriteResponse
from app.schemas.response import ApiResponse

from app.services.favorite_service import (
    add_favorite,
    get_user_favorites,
    remove_favorite
)

from app.utils.response import success_response

router = APIRouter(
    prefix="/api/favorites",
    tags=["Favorites"]
)

@router.post(
    "/{movie_id}",
    response_model=ApiResponse[FavoriteResponse],
    status_code=status.HTTP_201_CREATED
)
def create_favorite(
    movie_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite, error = add_favorite(
        db,
        current_user.id,
        movie_id
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
            if error == "Movie not found"
            else status.HTTP_409_CONFLICT,
            detail=error
        )

    return success_response(
        request=request,
        status=status.HTTP_201_CREATED,
        message="Movie added to favorites successfully",
        data=FavoriteResponse.model_validate(favorite)
    )

@router.get(
    "",
    response_model=ApiResponse[list[FavoriteResponse]],
    status_code=status.HTTP_200_OK
)
def get_favorites(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorites = get_user_favorites(
        db,
        current_user.id
    )

    return success_response(
        request=request,
        status=status.HTTP_200_OK,
        message="Favorites retrieved successfully",
        data=[
            FavoriteResponse.model_validate(favorite)
            for favorite in favorites
        ]
    )


@router.delete(
    "/{movie_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK
)
def delete_favorite(
    movie_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = remove_favorite(
        db,
        current_user.id,
        movie_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    return success_response(
        request=request,
        status=status.HTTP_200_OK,
        message="Movie removed from favorites successfully"
    )