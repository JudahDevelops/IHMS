from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.staff_profile_controller import staff_profile_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.staff_profile import (
    StaffProfileCreate,
    StaffProfileUpdate,
    StaffProfileResponse,
)

router = APIRouter(prefix="/staff-profiles", tags=["Staff Profiles"])

@router.get("", response_model=PaginatedResponse[StaffProfileResponse])
def get_staff_profiles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across staff number, designation, office"),
    unit_id: Optional[int] = Query(None, description="Filter by maintenance unit ID"),
    assigned_hostel_id: Optional[int] = Query(None, description="Filter by hostel ID"),
    db: Session = Depends(get_db),
):
    """Retrieve staff profiles with real-time search, filters, and optimized pagination."""
    filters = {}
    if unit_id is not None:
        filters["unit_id"] = unit_id
    if assigned_hostel_id is not None:
        filters["assigned_hostel_id"] = assigned_hostel_id
    return staff_profile_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=StaffProfileResponse)
def get_staff_profile(id: int, db: Session = Depends(get_db)):
    """Retrieve a single staff profile by ID."""
    return staff_profile_controller.get_by_id(db, id)

@router.post("", response_model=StaffProfileResponse, status_code=status.HTTP_201_CREATED)
def create_staff_profile(profile_in: StaffProfileCreate, db: Session = Depends(get_db)):
    """Insert a new staff profile."""
    return staff_profile_controller.create(db, obj_in=profile_in)

@router.put("/{id}", response_model=StaffProfileResponse)
def update_staff_profile(id: int, profile_in: StaffProfileUpdate, db: Session = Depends(get_db)):
    """Update an existing staff profile."""
    return staff_profile_controller.update(db, id=id, obj_in=profile_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_staff_profile(id: int, db: Session = Depends(get_db)):
    """Delete a single staff profile by ID."""
    return staff_profile_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_staff_profiles(
    confirm: bool = Query(False, description="Must be true to confirm deleting all staff profiles"),
    db: Session = Depends(get_db),
):
    """Delete all staff profiles (requires confirmation flag)."""
    return staff_profile_controller.delete_all(db, confirm=confirm)

