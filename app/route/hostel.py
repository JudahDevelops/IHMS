from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.hostel_controller import hostel_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.hostel import HostelCreate, HostelUpdate, HostelResponse

router = APIRouter(prefix="/hostels", tags=["Hostels"])

@router.get("", response_model=PaginatedResponse[HostelResponse])
def get_hostels(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across name, code, description, gender"),
    db: Session = Depends(get_db),
):
    """Retrieve hostels with real-time search and optimized pagination."""
    return hostel_controller.get_paginated(db, page=page, page_size=page_size, search=search)

@router.get("/{id}", response_model=HostelResponse)
def get_hostel(id: int, db: Session = Depends(get_db)):
    """Retrieve a single hostel by ID."""
    return hostel_controller.get_by_id(db, id)

@router.post("", response_model=HostelResponse, status_code=status.HTTP_201_CREATED)
def create_hostel(hostel_in: HostelCreate, db: Session = Depends(get_db)):
    """Insert a new hostel."""
    return hostel_controller.create(db, obj_in=hostel_in)

@router.put("/{id}", response_model=HostelResponse)
def update_hostel(id: int, hostel_in: HostelUpdate, db: Session = Depends(get_db)):
    """Update an existing hostel."""
    return hostel_controller.update(db, id=id, obj_in=hostel_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_hostel(id: int, db: Session = Depends(get_db)):
    """Delete a single hostel by ID."""
    return hostel_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_hostels(
    confirm: bool = Query(False, description="Must be true to confirm deleting all hostels"),
    db: Session = Depends(get_db),
):
    """Delete all hostels (requires confirmation flag)."""
    return hostel_controller.delete_all(db, confirm=confirm)

