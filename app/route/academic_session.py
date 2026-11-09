from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.academic_session_controller import academic_session_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.academic_session import (
    AcademicSessionCreate,
    AcademicSessionUpdate,
    AcademicSessionResponse,
)

router = APIRouter(prefix="/academic-sessions", tags=["Academic Sessions"])

@router.get("", response_model=PaginatedResponse[AcademicSessionResponse])
def get_academic_sessions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across session name and semester"),
    is_current: Optional[bool] = Query(None, description="Filter current session"),
    db: Session = Depends(get_db),
):
    """Retrieve academic sessions with real-time search, filters, and optimized pagination."""
    filters = {}
    if is_current is not None:
        filters["is_current"] = is_current
    return academic_session_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=AcademicSessionResponse)
def get_academic_session(id: int, db: Session = Depends(get_db)):
    """Retrieve a single academic session by ID."""
    return academic_session_controller.get_by_id(db, id)

@router.post("", response_model=AcademicSessionResponse, status_code=status.HTTP_201_CREATED)
def create_academic_session(session_in: AcademicSessionCreate, db: Session = Depends(get_db)):
    """Insert a new academic session."""
    return academic_session_controller.create(db, obj_in=session_in)

@router.put("/{id}", response_model=AcademicSessionResponse)
def update_academic_session(id: int, session_in: AcademicSessionUpdate, db: Session = Depends(get_db)):
    """Update an existing academic session."""
    return academic_session_controller.update(db, id=id, obj_in=session_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_academic_session(id: int, db: Session = Depends(get_db)):
    """Delete a single academic session by ID."""
    return academic_session_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_academic_sessions(
    confirm: bool = Query(False, description="Must be true to confirm deleting all academic sessions"),
    db: Session = Depends(get_db),
):
    """Delete all academic sessions (requires confirmation flag)."""
    return academic_session_controller.delete_all(db, confirm=confirm)

