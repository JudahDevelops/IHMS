from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.bed_space_controller import bed_space_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.bed_space import BedSpaceCreate, BedSpaceUpdate, BedSpaceResponse

router = APIRouter(prefix="/bed-spaces", tags=["Bed Spaces"])

@router.get("", response_model=PaginatedResponse[BedSpaceResponse])
def get_bed_spaces(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across bed label"),
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    is_occupied: Optional[bool] = Query(None, description="Filter by occupancy status"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
):
    """Retrieve bed spaces with real-time search, filters, and optimized pagination."""
    filters = {}
    if room_id is not None:
        filters["room_id"] = room_id
    if is_occupied is not None:
        filters["is_occupied"] = is_occupied
    if is_active is not None:
        filters["is_active"] = is_active
    return bed_space_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=BedSpaceResponse)
def get_bed_space(id: int, db: Session = Depends(get_db)):
    """Retrieve a single bed space by ID."""
    return bed_space_controller.get_by_id(db, id)

@router.post("", response_model=BedSpaceResponse, status_code=status.HTTP_201_CREATED)
def create_bed_space(bed_space_in: BedSpaceCreate, db: Session = Depends(get_db)):
    """Insert a new bed space."""
    return bed_space_controller.create(db, obj_in=bed_space_in)

@router.put("/{id}", response_model=BedSpaceResponse)
def update_bed_space(id: int, bed_space_in: BedSpaceUpdate, db: Session = Depends(get_db)):
    """Update an existing bed space."""
    return bed_space_controller.update(db, id=id, obj_in=bed_space_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_bed_space(id: int, db: Session = Depends(get_db)):
    """Delete a single bed space by ID."""
    return bed_space_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_bed_spaces(
    confirm: bool = Query(False, description="Must be true to confirm deleting all bed spaces"),
    db: Session = Depends(get_db),
):
    """Delete all bed spaces (requires confirmation flag)."""
    return bed_space_controller.delete_all(db, confirm=confirm)

