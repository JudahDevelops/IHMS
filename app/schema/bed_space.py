from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class BedSpaceBase(BaseModel):
    room_id: int
    bed_label: str = Field(..., max_length=10)
    is_occupied: bool = False
    is_active: bool = True

class BedSpaceCreate(BedSpaceBase):
    pass

class BedSpaceUpdate(BaseModel):
    room_id: Optional[int] = None
    bed_label: Optional[str] = Field(None, max_length=10)
    is_occupied: Optional[bool] = None
    is_active: Optional[bool] = None

class BedSpaceResponse(BedSpaceBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

