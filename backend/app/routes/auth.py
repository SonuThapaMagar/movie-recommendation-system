from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import UserResgister,UserResponse
from app.services.auth_service import register_user
from app.schemas.response import ApiResponse
from app.utils.response import success_response
from fastapi import Request

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED
)
def register(request: Request,user_data:UserResgister,db:Session=Depends(get_db)):
    user,error=register_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )
    
    if error:
        field = "username" if "Username" in error else "email"

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": error,
                "errors": [
                    {
                        "field": field,
                        "message": error
                    }
                ]
            }
        )

    return success_response(
        request=request,
        status=status.HTTP_201_CREATED,
        message="User registered successfully",
        data=UserResponse.model_validate(user)
    )