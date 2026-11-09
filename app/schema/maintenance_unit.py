from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class MaintenanceUnitBase(BaseModel):
    code: str = Field(..., max_length=30)
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    email: str = Field(..., max_length=100)
    is_active: bool = True

class MaintenanceUnitCreate(MaintenanceUnitBase):
    pass

class MaintenanceUnitUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=30)
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class MaintenanceUnitResponse(MaintenanceUnitBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

