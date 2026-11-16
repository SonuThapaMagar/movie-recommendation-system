from datetime import datetime,timezone
from typing import Generic,TypeVar

from pydantic import BaseModel,Field

T=TypeVar("T")

class ErrorDetail(BaseModel):
    field:str|None=None
    message:str

class PaginationMeta(BaseModel):
    page:int
    per_page:int
    total:int
    total_pages:int
    
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    status: int
    message: str
    data: T | None = None
    errors: list[ErrorDetail] | None = None
    pagination: PaginationMeta | None = None
    timestamp: datetime = Field( default_factory=lambda: datetime.now(timezone.utc))
    path: str | None = None