from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.complaint_history_controller import complaint_history_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.complaint_history import (
    ComplaintHistoryCreate,
    ComplaintHistoryUpdate,
    ComplaintHistoryResponse,
)

router = APIRouter(prefix="/complaint-history", tags=["Complaint History"])

@router.get("", response_model=PaginatedResponse[ComplaintHistoryResponse])
def get_complaint_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across action type, statuses, notes"),
    complaint_id: Optional[int] = Query(None, description="Filter by complaint ID"),
    performed_by_user_id: Optional[int] = Query(None, description="Filter by user ID"),
    db: Session = Depends(get_db),
):
    """Retrieve complaint history entries with real-time search, filters, and optimized pagination."""
    filters = {}
    if complaint_id is not None:
        filters["complaint_id"] = complaint_id
    if performed_by_user_id is not None:
        filters["performed_by_user_id"] = performed_by_user_id
    return complaint_history_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=ComplaintHistoryResponse)
def get_complaint_history_item(id: int, db: Session = Depends(get_db)):
    """Retrieve a single complaint history entry by ID."""
    return complaint_history_controller.get_by_id(db, id)

@router.post("", response_model=ComplaintHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_complaint_history(item_in: ComplaintHistoryCreate, db: Session = Depends(get_db)):
    """Insert a new complaint history entry."""
    return complaint_history_controller.create(db, obj_in=item_in)

@router.put("/{id}", response_model=ComplaintHistoryResponse)
def update_complaint_history(id: int, item_in: ComplaintHistoryUpdate, db: Session = Depends(get_db)):
    """Update an existing complaint history entry."""
    return complaint_history_controller.update(db, id=id, obj_in=item_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_complaint_history(id: int, db: Session = Depends(get_db)):
    """Delete a single complaint history entry by ID."""
    return complaint_history_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_complaint_history(
    confirm: bool = Query(False, description="Must be true to confirm deleting all history entries"),
    db: Session = Depends(get_db),
):
    """Delete all complaint history entries (requires confirmation flag)."""
    return complaint_history_controller.delete_all(db, confirm=confirm)

