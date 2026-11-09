from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.maintenance_unit_controller import maintenance_unit_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.maintenance_unit import (
    MaintenanceUnitCreate,
    MaintenanceUnitUpdate,
    MaintenanceUnitResponse,
)

router = APIRouter(prefix="/maintenance-units", tags=["Maintenance Units"])

@router.get("", response_model=PaginatedResponse[MaintenanceUnitResponse])
def get_maintenance_units(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across code, name, description, email"),
    db: Session = Depends(get_db),
):
    """Retrieve maintenance units with real-time search and optimized pagination."""
    return maintenance_unit_controller.get_paginated(db, page=page, page_size=page_size, search=search)

@router.get("/{id}", response_model=MaintenanceUnitResponse)
def get_maintenance_unit(id: int, db: Session = Depends(get_db)):
    """Retrieve a single maintenance unit by ID."""
    return maintenance_unit_controller.get_by_id(db, id)

@router.post("", response_model=MaintenanceUnitResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance_unit(unit_in: MaintenanceUnitCreate, db: Session = Depends(get_db)):
    """Insert a new maintenance unit."""
    return maintenance_unit_controller.create(db, obj_in=unit_in)

@router.put("/{id}", response_model=MaintenanceUnitResponse)
def update_maintenance_unit(id: int, unit_in: MaintenanceUnitUpdate, db: Session = Depends(get_db)):
    """Update an existing maintenance unit."""
    return maintenance_unit_controller.update(db, id=id, obj_in=unit_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_maintenance_unit(id: int, db: Session = Depends(get_db)):
    """Delete a single maintenance unit by ID."""
    return maintenance_unit_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_maintenance_units(
    confirm: bool = Query(False, description="Must be true to confirm deleting all maintenance units"),
    db: Session = Depends(get_db),
):
    """Delete all maintenance units (requires confirmation flag)."""
    return maintenance_unit_controller.delete_all(db, confirm=confirm)

