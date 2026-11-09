from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import StudentGenderEnum

class StudentProfileBase(BaseModel):
    user_id: int
    matric_number: str = Field(..., max_length=50)
    gender: StudentGenderEnum
    level: int = Field(..., description="Academic level e.g. 100, 200, 300, 400, 500")
    department: str = Field(..., max_length=100)
    faculty: Optional[str] = Field(None, max_length=100)
    fee_cleared: bool = False
    fee_cleared_at: Optional[datetime] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileUpdate(BaseModel):
    user_id: Optional[int] = None
    matric_number: Optional[str] = Field(None, max_length=50)
    gender: Optional[StudentGenderEnum] = None
    level: Optional[int] = None
    department: Optional[str] = Field(None, max_length=100)
    faculty: Optional[str] = Field(None, max_length=100)
    fee_cleared: Optional[bool] = None
    fee_cleared_at: Optional[datetime] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)

class StudentProfileResponse(StudentProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

