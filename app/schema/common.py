import math
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")

class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None

class DeleteAllResponse(BaseModel):
    message: str
    deleted_count: int

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int = Field(..., description="Total number of items matching query")
    page: int = Field(..., description="Current page number (1-indexed)")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether a next page exists")
    has_prev: bool = Field(..., description="Whether a previous page exists")

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )

