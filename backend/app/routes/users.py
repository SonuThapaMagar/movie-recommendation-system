
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.user import (
    UserUpdate,
    UserProfileResponse
)

from app.schemas.response import ApiResponse

from app.services.user_service import (
    get_user_profile,
    update_user_profile,
    delete_user_account
)

from app.utils.response import (
    success_response,
    error_response
)


router = APIRouter(prefix="/api/users",tags=["Users"])


# GET USER PROFILE
@router.get(
    "/me",
    response_model=ApiResponse[UserProfileResponse]
)
def get_my_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = get_user_profile(db, current_user.id)

    if not user:
        return error_response(
            request,
            status=404,
            message="User not found"
        )

    return success_response(
        request,
        status.HTTP_200_OK,
        "User profile retrieved successfully",
        user
    )


# UPDATE USER PROFILE
@router.put(
    "/me",
    response_model=ApiResponse[UserProfileResponse]
)
def update_my_profile(
    update_data: UserUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    data = update_data.model_dump(exclude_unset=True)

    if not data:
        return error_response(
            request,
            status=400,
            message="Provide at least one field to update"
        )

    user, error = update_user_profile(
        db,
        current_user.id,
        data
    )

    if error:
        error_status = 404 if error == "User not found" else 409

        return error_response(
            request,
            status=error_status,
            message=error
        )

    return success_response(
        request,
        status.HTTP_200_OK,
        "User profile updated successfully",
        user
    )


# DELETE USER ACCOUNT
@router.delete(
    "/me",
    response_model=ApiResponse[None]
)
def delete_my_account(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    deleted = delete_user_account(
        db,
        current_user.id
    )

    if not deleted:
        return error_response(
            request,
            status=404,
            message="User not found"
        )

    return success_response(
        request,
        status.HTTP_200_OK,
        "User account deleted successfully"
    )
