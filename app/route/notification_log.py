from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controller.notification_log_controller import notification_log_controller
from app.model.enums import NotificationEventEnum, DeliveryStatusEnum
from app.schema.common import PaginatedResponse, MessageResponse, DeleteAllResponse
from app.schema.notification_log import (
    NotificationLogCreate,
    NotificationLogUpdate,
    NotificationLogResponse,
)

router = APIRouter(prefix="/notification-logs", tags=["Notification Logs"])

@router.get("", response_model=PaginatedResponse[NotificationLogResponse])
def get_notification_logs(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Real-time search across recipient, subject, body, status"),
    recipient_user_id: Optional[int] = Query(None, description="Filter by recipient user ID"),
    complaint_id: Optional[int] = Query(None, description="Filter by complaint ID"),
    event_type: Optional[NotificationEventEnum] = Query(None, description="Filter by event type"),
    delivery_status: Optional[DeliveryStatusEnum] = Query(None, alias="status", description="Filter by delivery status"),
    db: Session = Depends(get_db),
):
    """Retrieve notification logs with real-time search, filters, and optimized pagination."""
    filters = {}
    if recipient_user_id is not None:
        filters["recipient_user_id"] = recipient_user_id
    if complaint_id is not None:
        filters["complaint_id"] = complaint_id
    if event_type is not None:
        filters["event_type"] = event_type
    if delivery_status is not None:
        filters["status"] = delivery_status
    return notification_log_controller.get_paginated(db, page=page, page_size=page_size, search=search, filters=filters)

@router.get("/{id}", response_model=NotificationLogResponse)
def get_notification_log(id: int, db: Session = Depends(get_db)):
    """Retrieve a single notification log by ID."""
    return notification_log_controller.get_by_id(db, id)

@router.post("", response_model=NotificationLogResponse, status_code=status.HTTP_201_CREATED)
def create_notification_log(log_in: NotificationLogCreate, db: Session = Depends(get_db)):
    """Insert a new notification log."""
    return notification_log_controller.create(db, obj_in=log_in)

@router.put("/{id}", response_model=NotificationLogResponse)
def update_notification_log(id: int, log_in: NotificationLogUpdate, db: Session = Depends(get_db)):
    """Update an existing notification log."""
    return notification_log_controller.update(db, id=id, obj_in=log_in)

@router.delete("/{id}", response_model=MessageResponse)
def delete_notification_log(id: int, db: Session = Depends(get_db)):
    """Delete a single notification log by ID."""
    return notification_log_controller.delete(db, id=id)

@router.delete("", response_model=DeleteAllResponse)
def delete_all_notification_logs(
    confirm: bool = Query(False, description="Must be true to confirm deleting all notification logs"),
    db: Session = Depends(get_db),
):
    """Delete all notification logs (requires confirmation flag)."""
    return notification_log_controller.delete_all(db, confirm=confirm)

