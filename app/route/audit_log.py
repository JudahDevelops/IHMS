from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.audit_log_controller import audit_log_controller
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.audit_log import (
    AuditLogCreate,
    AuditLogUpdate,
    AuditLogResponse,
)

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("", response_model=PaginatedResponse[AuditLogResponse])
def get_audit_logs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across action, entity, IP, and values"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    entity_name: Optional[str] = Query(None, description="Filter by entity name"),
    action: Optional[str] = Query(None, description="Filter by action"),
    db: Session = Depends(get_db),
):
    """Retrieve audit logs with real-time search, filters, and optimized pagination."""
    filters = {}
    if user_id is not None:
        filters["user_id"] = user_id
    if entity_name is not None:
        filters["entity_name"] = entity_name
    if action is not None:
        filters["action"] = action
    return audit_log_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=AuditLogResponse)
def get_audit_log(id: int, db: Session = Depends(get_db)):
    """Retrieve a single audit log by ID."""
    return audit_log_controller.get_by_id(db, id)

@router.post("", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
def create_audit_log(log_in: AuditLogCreate, db: Session = Depends(get_db)):
    """Insert a new audit log."""
    return audit_log_controller.create(db, obj_in=log_in)

@router.put("/{id}", response_model=AuditLogResponse)
def update_audit_log(id: int, log_in: AuditLogUpdate, db: Session = Depends(get_db)):
    """Update an existing audit log."""
    return audit_log_controller.update(db, id=id, obj_in=log_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_audit_log(id: int, db: Session = Depends(get_db)):
    """Delete a single audit log by ID."""
    return audit_log_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_audit_logs(
    confirm: bool = Query(False, description="Must be true to confirm deleting all audit logs"),
    db: Session = Depends(get_db),
):
    """Delete all audit logs (requires confirmation flag)."""
    return audit_log_controller.delete_all(db, confirm=confirm)

