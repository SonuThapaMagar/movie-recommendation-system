from fastapi import Request
from app.schemas.response import ApiResponse,ErrorDetail

def success_response(
    request:Request,
    status:int,
    message:str,
    data=None
):
    return ApiResponse(
        success=True,
        status=status,
        message=message,
        data=data,
        errors=None,
        pagination=None,
        path=request.url.path
    )
    
def error_response(
    request: Request,
    status: int,
    message: str,
    errors: list[ErrorDetail] | None = None
):
    return ApiResponse(
        success=False,
        status=status,
        message=message,
        data=None,
        errors=errors,
        pagination=None,
        path=request.url.path
    )