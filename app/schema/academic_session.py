from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import SemesterEnum

class AcademicSessionBase(BaseModel):
    session_name: str = Field(..., max_length=50, description="e.g. 2024/2025")
    semester: SemesterEnum = SemesterEnum.FIRST
    is_current: bool = False
    start_date: date
    end_date: date

class AcademicSessionCreate(AcademicSessionBase):
    pass

class AcademicSessionUpdate(BaseModel):
    session_name: Optional[str] = Field(None, max_length=50)
    semester: Optional[SemesterEnum] = None
    is_current: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class AcademicSessionResponse(AcademicSessionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

