from fastapi import APIRouter,Depends,HTTPException,Request,status,Response
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.rating import Rating
from app.schemas.rating import RatingCreate,UserRatingResponse
from app.schemas.response import ApiResponse
from app.services.rating_service import (add_or_update_rating,get_user_ratings,get_user_movie_rating,delete_user_rating)
from app.utils.response import success_response

router=APIRouter(prefix="/api/ratings",tags=["Ratings"])

@router.post("/{movie_id}",response_model=ApiResponse[UserRatingResponse])
def rate_movie(movie_id:int,rating_data:RatingCreate,request:Request,response: Response,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    rating, created, error = add_or_update_rating(
    db,
    current_user.id,
    movie_id,
    rating_data.rating
)
    
    if error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=error)
        
    message = (
        "Movie rated successfully"
        if created
        else "Movie rating updated successfully"
    )

    
    response_status = (
        status.HTTP_201_CREATED
        if created
        else status.HTTP_200_OK
    )
    
    return success_response(
        request,
        response_status,
        message,
        rating
    )
    
@router.get(
    "/me",
    response_model=ApiResponse[list[UserRatingResponse]]
)
def get_my_ratings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ratings = get_user_ratings(db, current_user.id)

    return success_response(
        request,
        status.HTTP_200_OK,
        "User ratings retrieved successfully",
        ratings
    )
    
@router.get(
    "/{movie_id}",
    response_model=ApiResponse[UserRatingResponse]
)
def get_movie_rating(
    movie_id:int,
    request:Request,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    rating=get_user_movie_rating(
        db,
        current_user.id,
        movie_id
    )
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return success_response(
        request,
        status.HTTP_200_OK,
        "Movie rating retrieved successfully",
        rating
    )

@router.delete("/{movie_id}",response_model=ApiResponse[None])
def remove_rating(
    movie_id:int,
    request:Request,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    deleted=delete_user_rating(
        db,
        current_user.id,
        movie_id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
        
    return success_response(
        request,
        status.HTTP_200_OK,
        "Movie rating deleted successfully"
    )