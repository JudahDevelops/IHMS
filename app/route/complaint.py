from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.complaint_controller import complaint_controller
from app.model.enums import (
    ComplaintCategoryEnum,
    ComplaintUrgencyEnum,
    ComplaintStatusEnum,
)
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)

router = APIRouter(prefix="/complaints", tags=["Complaints"])

@router.get("", response_model=PaginatedResponse[ComplaintResponse])
def get_complaints(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across code, title, description, category, urgency, status"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    room_id: Optional[int] = Query(None, description="Filter by room ID"),
    assigned_unit_id: Optional[int] = Query(None, description="Filter by maintenance unit ID"),
    category: Optional[ComplaintCategoryEnum] = Query(None, description="Filter by category"),
    urgency: Optional[ComplaintUrgencyEnum] = Query(None, description="Filter by urgency"),
    complaint_status: Optional[ComplaintStatusEnum] = Query(None, alias="status", description="Filter by status"),
    escalation_level: Optional[int] = Query(None, description="Filter by escalation level"),
    db: Session = Depends(get_db),
):
    """Retrieve complaints with real-time search, filters, and optimized pagination."""
    filters = {}
    if student_id is not None:
        filters["student_id"] = student_id
    if room_id is not None:
        filters["room_id"] = room_id
    if assigned_unit_id is not None:
        filters["assigned_unit_id"] = assigned_unit_id
    if category is not None:
        filters["category"] = category
    if urgency is not None:
        filters["urgency"] = urgency
    if complaint_status is not None:
        filters["status"] = complaint_status
    if escalation_level is not None:
        filters["escalation_level"] = escalation_level
    return complaint_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=ComplaintResponse)
def get_complaint(id: int, db: Session = Depends(get_db)):
    """Retrieve a single complaint by ID."""
    return complaint_controller.get_by_id(db, id)

@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(complaint_in: ComplaintCreate, db: Session = Depends(get_db)):
    """Insert a new complaint."""
    return complaint_controller.create(db, obj_in=complaint_in)

@router.put("/{id}", response_model=ComplaintResponse)
def update_complaint(id: int, complaint_in: ComplaintUpdate, db: Session = Depends(get_db)):
    """Update an existing complaint."""
    return complaint_controller.update(db, id=id, obj_in=complaint_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_complaint(id: int, db: Session = Depends(get_db)):
    """Delete a single complaint by ID."""
    return complaint_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_complaints(
    confirm: bool = Query(False, description="Must be true to confirm deleting all complaints"),
    db: Session = Depends(get_db),
):
    """Delete all complaints (requires confirmation flag)."""
    return complaint_controller.delete_all(db, confirm=confirm)

