from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import ComplaintCategoryEnum, ComplaintUrgencyEnum

class TriageKeywordBase(BaseModel):
    keyword: str = Field(..., max_length=100)
    category: ComplaintCategoryEnum
    urgency: ComplaintUrgencyEnum
    weight: int = 1
    is_active: bool = True

class TriageKeywordCreate(TriageKeywordBase):
    pass

class TriageKeywordUpdate(BaseModel):
    keyword: Optional[str] = Field(None, max_length=100)
    category: Optional[ComplaintCategoryEnum] = None
    urgency: Optional[ComplaintUrgencyEnum] = None
    weight: Optional[int] = None
    is_active: Optional[bool] = None

class TriageKeywordResponse(TriageKeywordBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

