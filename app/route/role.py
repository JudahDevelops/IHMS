from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.role_controller import role_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("", response_model=PaginatedResponse[RoleResponse])
def get_roles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search keyword"),
    db: Session = Depends(get_db),
):
    """Retrieve roles with real-time search and optimized pagination."""
    return role_controller.get_paginated(db, page=page, page_size=page_size, search=search)

@router.get("/{id}", response_model=RoleResponse)
def get_role(id: int, db: Session = Depends(get_db)):
    """Retrieve a single role by ID."""
    return role_controller.get_by_id(db, id)

@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    """Insert a new role."""
    return role_controller.create(db, obj_in=role_in)

@router.put("/{id}", response_model=RoleResponse)
def update_role(id: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    """Update an existing role."""
    return role_controller.update(db, id=id, obj_in=role_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_role(id: int, db: Session = Depends(get_db)):
    """Delete a single role by ID."""
    return role_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_roles(
    confirm: bool = Query(False, description="Must be true to confirm deleting all roles"),
    db: Session = Depends(get_db),
):
    """Delete all roles (requires confirmation flag)."""
    return role_controller.delete_all(db, confirm=confirm)

