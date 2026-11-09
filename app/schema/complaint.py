from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import (
    ComplaintCategoryEnum,
    ComplaintUrgencyEnum,
    TriageSourceEnum,
    ComplaintStatusEnum,
)

class ComplaintBase(BaseModel):
    student_id: int
    room_id: int
    title: str = Field(..., max_length=150)
    description: str
    category: ComplaintCategoryEnum
    urgency: ComplaintUrgencyEnum
    assigned_unit_id: int
    complaint_code: Optional[str] = Field(None, max_length=50)
    triage_source: TriageSourceEnum = TriageSourceEnum.MANUAL
    triage_confidence: Optional[float] = None
    assigned_officer_id: Optional[int] = None
    status: ComplaintStatusEnum = ComplaintStatusEnum.OPEN
    escalation_level: int = 0
    deadline_at: Optional[datetime] = None
    escalated_to_warden_at: Optional[datetime] = None
    escalated_to_admin_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    student_feedback_rating: Optional[int] = Field(None, ge=1, le=5)
    student_feedback_comment: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    pass

class ComplaintUpdate(BaseModel):
    student_id: Optional[int] = None
    room_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = None
    category: Optional[ComplaintCategoryEnum] = None
    urgency: Optional[ComplaintUrgencyEnum] = None
    triage_source: Optional[TriageSourceEnum] = None
    triage_confidence: Optional[float] = None
    assigned_unit_id: Optional[int] = None
    assigned_officer_id: Optional[int] = None
    status: Optional[ComplaintStatusEnum] = None
    escalation_level: Optional[int] = None
    deadline_at: Optional[datetime] = None
    escalated_to_warden_at: Optional[datetime] = None
    escalated_to_admin_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    student_feedback_rating: Optional[int] = Field(None, ge=1, le=5)
    student_feedback_comment: Optional[str] = None

class ComplaintResponse(ComplaintBase):
    id: int
    complaint_code: str
    submitted_at: datetime

    model_config = ConfigDict(from_attributes=True)

