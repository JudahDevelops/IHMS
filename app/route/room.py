from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.room_controller import room_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.room import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.get("", response_model=PaginatedResponse[RoomResponse])
def get_rooms(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across room number"),
    hostel_id: Optional[int] = Query(None, description="Filter by hostel ID"),
    is_available: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_db),
):
    """Retrieve rooms with real-time search, filters, and optimized pagination."""
    filters = {}
    if hostel_id is not None:
        filters["hostel_id"] = hostel_id
    if is_available is not None:
        filters["is_available"] = is_available
    return room_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=RoomResponse)
def get_room(id: int, db: Session = Depends(get_db)):
    """Retrieve a single room by ID."""
    return room_controller.get_by_id(db, id)

@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room_in: RoomCreate, db: Session = Depends(get_db)):
    """Insert a new room."""
    return room_controller.create(db, obj_in=room_in)

@router.put("/{id}", response_model=RoomResponse)
def update_room(id: int, room_in: RoomUpdate, db: Session = Depends(get_db)):
    """Update an existing room."""
    return room_controller.update(db, id=id, obj_in=room_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_room(id: int, db: Session = Depends(get_db)):
    """Delete a single room by ID."""
    return room_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_rooms(
    confirm: bool = Query(False, description="Must be true to confirm deleting all rooms"),
    db: Session = Depends(get_db),
):
    """Delete all rooms (requires confirmation flag)."""
    return room_controller.delete_all(db, confirm=confirm)

