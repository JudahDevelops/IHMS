from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.student_profile_controller import student_profile_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.student_profile import (
    StudentProfileCreate,
    StudentProfileUpdate,
    StudentProfileResponse,
)

router = APIRouter(prefix="/student-profiles", tags=["Student Profiles"])

@router.get("", response_model=PaginatedResponse[StudentProfileResponse])
def get_student_profiles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across matric number, department, faculty, contacts"),
    fee_cleared: Optional[bool] = Query(None, description="Filter by fee clearance status"),
    level: Optional[int] = Query(None, description="Filter by level"),
    db: Session = Depends(get_db),
):
    """Retrieve student profiles with real-time search, filters, and optimized pagination."""
    filters = {}
    if fee_cleared is not None:
        filters["fee_cleared"] = fee_cleared
    if level is not None:
        filters["level"] = level
    return student_profile_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=StudentProfileResponse)
def get_student_profile(id: int, db: Session = Depends(get_db)):
    """Retrieve a single student profile by ID."""
    return student_profile_controller.get_by_id(db, id)

@router.post("", response_model=StudentProfileResponse, status_code=status.HTTP_201_CREATED)
def create_student_profile(profile_in: StudentProfileCreate, db: Session = Depends(get_db)):
    """Insert a new student profile."""
    return student_profile_controller.create(db, obj_in=profile_in)

@router.put("/{id}", response_model=StudentProfileResponse)
def update_student_profile(id: int, profile_in: StudentProfileUpdate, db: Session = Depends(get_db)):
    """Update an existing student profile."""
    return student_profile_controller.update(db, id=id, obj_in=profile_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_student_profile(id: int, db: Session = Depends(get_db)):
    """Delete a single student profile by ID."""
    return student_profile_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_student_profiles(
    confirm: bool = Query(False, description="Must be true to confirm deleting all student profiles"),
    db: Session = Depends(get_db),
):
    """Delete all student profiles (requires confirmation flag)."""
    return student_profile_controller.delete_all(db, confirm=confirm)

