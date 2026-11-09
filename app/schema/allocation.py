from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import AllocationStatusEnum

class AllocationBase(BaseModel):
    student_id: int
    bed_space_id: int
    session_id: int
    status: AllocationStatusEnum = AllocationStatusEnum.ACTIVE
    expires_at: Optional[datetime] = None
    checked_in_at: Optional[datetime] = None
    checked_out_at: Optional[datetime] = None
    allocated_by_user_id: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=255)

class AllocationCreate(AllocationBase):
    pass

class AllocationUpdate(BaseModel):
    student_id: Optional[int] = None
    bed_space_id: Optional[int] = None
    session_id: Optional[int] = None
    status: Optional[AllocationStatusEnum] = None
    expires_at: Optional[datetime] = None
    checked_in_at: Optional[datetime] = None
    checked_out_at: Optional[datetime] = None
    allocated_by_user_id: Optional[int] = None
    notes: Optional[str] = Field(None, max_length=255)

class AllocationResponse(AllocationBase):
    id: int
    active_bed_marker: Optional[int] = None
    active_student_session_marker: Optional[str] = None
    allocated_at: datetime

    model_config = ConfigDict(from_attributes=True)

