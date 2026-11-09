from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class StaffProfileBase(BaseModel):
    user_id: int
    staff_number: str = Field(..., max_length=50)
    unit_id: Optional[int] = None
    assigned_hostel_id: Optional[int] = None
    designation: Optional[str] = Field(None, max_length=100)
    office_location: Optional[str] = Field(None, max_length=100)

class StaffProfileCreate(StaffProfileBase):
    pass

class StaffProfileUpdate(BaseModel):
    user_id: Optional[int] = None
    staff_number: Optional[str] = Field(None, max_length=50)
    unit_id: Optional[int] = None
    assigned_hostel_id: Optional[int] = None
    designation: Optional[str] = Field(None, max_length=100)
    office_location: Optional[str] = Field(None, max_length=100)

class StaffProfileResponse(StaffProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

