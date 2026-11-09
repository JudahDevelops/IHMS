from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import NotificationEventEnum, DeliveryStatusEnum

class NotificationLogBase(BaseModel):
    recipient_email: str = Field(..., max_length=100)
    recipient_role: str = Field(..., max_length=50)
    recipient_user_id: Optional[int] = None
    subject: str = Field(..., max_length=200)
    body: str
    event_type: NotificationEventEnum
    complaint_id: Optional[int] = None
    status: DeliveryStatusEnum = DeliveryStatusEnum.QUEUED
    error_message: Optional[str] = None

class NotificationLogCreate(NotificationLogBase):
    pass

class NotificationLogUpdate(BaseModel):
    recipient_email: Optional[str] = Field(None, max_length=100)
    recipient_role: Optional[str] = Field(None, max_length=50)
    recipient_user_id: Optional[int] = None
    subject: Optional[str] = Field(None, max_length=200)
    body: Optional[str] = None
    event_type: Optional[NotificationEventEnum] = None
    complaint_id: Optional[int] = None
    status: Optional[DeliveryStatusEnum] = None
    error_message: Optional[str] = None

class NotificationLogResponse(NotificationLogBase):
    id: int
    sent_at: datetime

    model_config = ConfigDict(from_attributes=True)

