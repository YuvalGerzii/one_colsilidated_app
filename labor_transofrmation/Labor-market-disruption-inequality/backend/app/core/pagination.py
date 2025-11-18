"""
Pagination utilities for API endpoints
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query
from math import ceil


T = TypeVar("T")


class PaginationParams(BaseModel):
    """Standard pagination parameters"""
    page: int = 1
    page_size: int = 20
    max_page_size: int = 100

    def __init__(self, **data):
        super().__init__(**data)
        # Ensure page is at least 1
        if self.page < 1:
            self.page = 1
        # Limit page size
        if self.page_size > self.max_page_size:
            self.page_size = self.max_page_size
        if self.page_size < 1:
            self.page_size = 20

    @property
    def offset(self) -> int:
        """Calculate offset for database query"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit for database query"""
        return self.page_size


class PageMetadata(BaseModel):
    """Metadata about pagination"""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    metadata: PageMetadata
    status: str = "success"

    class Config:
        arbitrary_types_allowed = True


def paginate(
    query: Query,
    page: int = 1,
    page_size: int = 20,
    max_page_size: int = 100
) -> tuple:
    """
    Paginate a SQLAlchemy query

    Returns:
        tuple: (items, total_count, pagination_params)
    """
    params = PaginationParams(page=page, page_size=page_size, max_page_size=max_page_size)

    # Get total count (before applying pagination)
    total_count = query.count()

    # Apply pagination to query
    items = query.offset(params.offset).limit(params.limit).all()

    return items, total_count, params


def create_pagination_metadata(
    page: int,
    page_size: int,
    total_items: int
) -> PageMetadata:
    """Create pagination metadata"""
    total_pages = ceil(total_items / page_size) if page_size > 0 else 0

    return PageMetadata(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1
    )


def create_paginated_response(
    items: List[T],
    total_count: int,
    page: int,
    page_size: int
) -> dict:
    """Create a standardized paginated response"""
    metadata = create_pagination_metadata(page, page_size, total_count)

    return {
        "status": "success",
        "items": items,
        "metadata": metadata.dict(),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_count,
            "total_pages": metadata.total_pages,
            "has_next": metadata.has_next,
            "has_previous": metadata.has_previous
        }
    }
