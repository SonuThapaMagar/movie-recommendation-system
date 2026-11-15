from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import UserResgister,UserResponse
from app.services.auth_service import register_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user_data:UserResgister,db:Session=Depends(get_db)):
    user,error=register_user(
        db=db,username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    if error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    
    return user