from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import ComplaintActionEnum

class ComplaintHistoryBase(BaseModel):
    complaint_id: int
    action_type: ComplaintActionEnum
    from_status: Optional[str] = Field(None, max_length=50)
    to_status: Optional[str] = Field(None, max_length=50)
    from_escalation_level: Optional[int] = None
    to_escalation_level: Optional[int] = None
    performed_by_user_id: Optional[int] = None
    notes: Optional[str] = None

class ComplaintHistoryCreate(ComplaintHistoryBase):
    pass

class ComplaintHistoryUpdate(BaseModel):
    complaint_id: Optional[int] = None
    action_type: Optional[ComplaintActionEnum] = None
    from_status: Optional[str] = Field(None, max_length=50)
    to_status: Optional[str] = Field(None, max_length=50)
    from_escalation_level: Optional[int] = None
    to_escalation_level: Optional[int] = None
    performed_by_user_id: Optional[int] = None
    notes: Optional[str] = None

class ComplaintHistoryResponse(ComplaintHistoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

