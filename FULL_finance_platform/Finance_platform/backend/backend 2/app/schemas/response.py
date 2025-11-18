"""Common response schemas."""

from typing import Generic, TypeVar, List, Any, Optional
from pydantic import BaseModel

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
