from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.response import ErrorDetail
from app.utils.response import error_response

async def http_Exception_handler(request:Request,exc:HTTPException):
    message="Request failed"
    errors=None
    
    if isinstance(exc.detail,dict):
        message=exc.detail.get("message",message)
        raw_errors=exc.detail.get("errors",[])
        errors=[ErrorDetail(**error) for error in raw_errors]
        
    elif isinstance(exc.detail, str):
        message = exc.detail
        
    response = error_response(
        request=request,
        status=exc.status_code,
        message=message,
        errors=errors
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json")
    )
    
async def validation_exception_handler(request:Request,exc:HTTPException):
    errors=[]
    for error in exc.errors():
        field=".".join(str(part) for part in error["loc"] if part !="body")
        
        errors.append(ErrorDetail(field=field,message=error["msg"]))
        
    response=error_response(request=request,status=422,message="Validation failed",errors=errors)
    
    return JSONResponse(
        status_code=422,
        content=response.model_dump(mode="json")
    )