from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.allocation_controller import allocation_controller
from app.model.enums import AllocationStatusEnum
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.allocation import (
    AllocationCreate,
    AllocationUpdate,
    AllocationResponse,
)

router = APIRouter(prefix="/allocations", tags=["Allocations"])

@router.get("", response_model=PaginatedResponse[AllocationResponse])
def get_allocations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across notes and status"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    bed_space_id: Optional[int] = Query(None, description="Filter by bed space ID"),
    session_id: Optional[int] = Query(None, description="Filter by academic session ID"),
    allocation_status: Optional[AllocationStatusEnum] = Query(None, alias="status", description="Filter by allocation status"),
    db: Session = Depends(get_db),
):
    """Retrieve allocations with real-time search, filters, and optimized pagination."""
    filters = {}
    if student_id is not None:
        filters["student_id"] = student_id
    if bed_space_id is not None:
        filters["bed_space_id"] = bed_space_id
    if session_id is not None:
        filters["session_id"] = session_id
    if allocation_status is not None:
        filters["status"] = allocation_status
    return allocation_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=AllocationResponse)
def get_allocation(id: int, db: Session = Depends(get_db)):
    """Retrieve a single allocation by ID."""
    return allocation_controller.get_by_id(db, id)

@router.post("", response_model=AllocationResponse, status_code=status.HTTP_201_CREATED)
def create_allocation(allocation_in: AllocationCreate, db: Session = Depends(get_db)):
    """Insert a new allocation."""
    return allocation_controller.create(db, obj_in=allocation_in)

@router.put("/{id}", response_model=AllocationResponse)
def update_allocation(id: int, allocation_in: AllocationUpdate, db: Session = Depends(get_db)):
    """Update an existing allocation."""
    return allocation_controller.update(db, id=id, obj_in=allocation_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_allocation(id: int, db: Session = Depends(get_db)):
    """Delete a single allocation by ID."""
    return allocation_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_allocations(
    confirm: bool = Query(False, description="Must be true to confirm deleting all allocations"),
    db: Session = Depends(get_db),
):
    """Delete all allocations (requires confirmation flag)."""
    return allocation_controller.delete_all(db, confirm=confirm)

