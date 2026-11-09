from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.user_controller import user_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=PaginatedResponse[UserResponse])
def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across username, email, name, phone"),
    db: Session = Depends(get_db),
):
    """Retrieve users with real-time search and optimized pagination."""
    return user_controller.get_paginated(db, page=page, page_size=page_size, search=search)

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    """Retrieve a single user by ID."""
    return user_controller.get_by_id(db, id)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Insert a new user."""
    return user_controller.create(db, obj_in=user_in)

@router.put("/{id}", response_model=UserResponse)
def update_user(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """Update an existing user."""
    return user_controller.update(db, id=id, obj_in=user_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    """Delete a single user by ID."""
    return user_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_users(
    confirm: bool = Query(False, description="Must be true to confirm deleting all users"),
    db: Session = Depends(get_db),
):
    """Delete all users (requires confirmation flag)."""
    return user_controller.delete_all(db, confirm=confirm)

