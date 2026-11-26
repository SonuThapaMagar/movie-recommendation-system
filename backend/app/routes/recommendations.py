from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from app.recommender.recommendation import (get_recommended_movies,user_item_matrix)
from app.database.database import get_db
from app.models.user  import User
from app.dependencies.auth import get_current_user

from app.services.recommendation_service import (
    get_recommendation_for_user
)

router=APIRouter(prefix="/api/recommendations",tags=["Recommendations"])

    
@router.get("/me")
def get_user_recommendations(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)):
    recommendations=get_recommendation_for_user(
        db=db,
        user_id=current_user.id,
        top_n=10
    )
    
    return {
        "user_id": current_user.id,
        "total": len(recommendations),
        "recommendations": recommendations
    }
