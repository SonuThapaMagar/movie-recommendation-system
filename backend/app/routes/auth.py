from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth import UserRegister,UserResponse
from app.services.auth_service import register_user
from app.schemas.response import ApiResponse
from app.utils.response import success_response
from fastapi import Request

from app.schemas.auth import UserLogin,TokenResponse
from app.services.auth_service import authenticate_user
from app.utils.security import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED
)
def register(request: Request,user_data:UserRegister,db:Session=Depends(get_db)):
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
    
#Login
@router.post("/login",response_model=ApiResponse[TokenResponse],status_code=status.HTTP_200_OK)
def login(request:Request,user_data:UserLogin,db:Session=Depends(get_db)):
    user=authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password")
    
    access_token=create_access_token(user.id)
    
    return success_response(
        request=request,
        status=status.HTTP_200_OK,
        message="Login successful",
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )
    
#Me
@router.get("/me",response_model=ApiResponse[UserResponse],status_code=status.HTTP_200_OK)
def get_me(request:Request,current_user: User = Depends(get_current_user)):
    return success_response(
        request=request,
        status=status.HTTP_200_OK,
        message="User retrieved successfully",
        data=UserResponse.model_validate(current_user)
    )

    