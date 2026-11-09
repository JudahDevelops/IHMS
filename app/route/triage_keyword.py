from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.triage_keyword_controller import triage_keyword_controller
from app.model.enums import ComplaintCategoryEnum, ComplaintUrgencyEnum
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.triage_keyword import (
    TriageKeywordCreate,
    TriageKeywordUpdate,
    TriageKeywordResponse,
)

router = APIRouter(prefix="/triage-keywords", tags=["Triage Keywords"])

@router.get("", response_model=PaginatedResponse[TriageKeywordResponse])
def get_triage_keywords(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across keyword, category, urgency"),
    category: Optional[ComplaintCategoryEnum] = Query(None, description="Filter by category"),
    urgency: Optional[ComplaintUrgencyEnum] = Query(None, description="Filter by urgency"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
):
    """Retrieve triage keywords with real-time search, filters, and optimized pagination."""
    filters = {}
    if category is not None:
        filters["category"] = category
    if urgency is not None:
        filters["urgency"] = urgency
    if is_active is not None:
        filters["is_active"] = is_active
    return triage_keyword_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=TriageKeywordResponse)
def get_triage_keyword(id: int, db: Session = Depends(get_db)):
    """Retrieve a single triage keyword by ID."""
    return triage_keyword_controller.get_by_id(db, id)

@router.post("", response_model=TriageKeywordResponse, status_code=status.HTTP_201_CREATED)
def create_triage_keyword(keyword_in: TriageKeywordCreate, db: Session = Depends(get_db)):
    """Insert a new triage keyword."""
    return triage_keyword_controller.create(db, obj_in=keyword_in)

@router.put("/{id}", response_model=TriageKeywordResponse)
def update_triage_keyword(id: int, keyword_in: TriageKeywordUpdate, db: Session = Depends(get_db)):
    """Update an existing triage keyword."""
    return triage_keyword_controller.update(db, id=id, obj_in=keyword_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_triage_keyword(id: int, db: Session = Depends(get_db)):
    """Delete a single triage keyword by ID."""
    return triage_keyword_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_triage_keywords(
    confirm: bool = Query(False, description="Must be true to confirm deleting all triage keywords"),
    db: Session = Depends(get_db),
):
    """Delete all triage keywords (requires confirmation flag)."""
    return triage_keyword_controller.delete_all(db, confirm=confirm)

