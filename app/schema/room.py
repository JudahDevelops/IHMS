from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class RoomBase(BaseModel):
    hostel_id: int
    room_number: str = Field(..., max_length=20)
    floor: int = 0
    capacity: int = 4
    current_occupancy: int = 0
    is_available: bool = True

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    hostel_id: Optional[int] = None
    room_number: Optional[str] = Field(None, max_length=20)
    floor: Optional[int] = None
    capacity: Optional[int] = None
    current_occupancy: Optional[int] = None
    is_available: Optional[bool] = None

class RoomResponse(RoomBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

