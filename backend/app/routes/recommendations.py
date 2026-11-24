from fastapi import APIRouter, HTTPException
from app.recommender.recommendation import (get_recommended_movies,user_item_matrix)

router=APIRouter(prefix="/api/recommendations",tags=["Recommendations"])

@router.get("/{user_id}")
def get_user_recommendations(user_id:int):
    #check whether the user exists
    if user_id not in user_item_matrix.index:
        raise HTTPException(
            status_code=404,
            detail="User not found in recommendation dataset"
        )
        
    #generate recommendations
    recommendations=get_recommended_movies(
        user_id=user_id,
        top_n=10
    )
    
    return{
        "user_id":user_id,
        "recommendations":recommendations
    }