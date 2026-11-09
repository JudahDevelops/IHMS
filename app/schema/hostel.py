from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.model.enums import HostelGenderEnum

class HostelBase(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    gender_target: HostelGenderEnum
    description: Optional[str] = Field(None, max_length=255)
    total_capacity: int = 0
    is_active: bool = True

class HostelCreate(HostelBase):
    pass

class HostelUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    code: Optional[str] = Field(None, max_length=20)
    gender_target: Optional[HostelGenderEnum] = None
    description: Optional[str] = Field(None, max_length=255)
    total_capacity: Optional[int] = None
    is_active: Optional[bool] = None

class HostelResponse(HostelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

