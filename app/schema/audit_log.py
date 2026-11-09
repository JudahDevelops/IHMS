from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    ip_address: Optional[str] = Field(None, max_length=50)
    action: str = Field(..., max_length=100)
    entity_name: str = Field(..., max_length=50)
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(BaseModel):
    user_id: Optional[int] = None
    ip_address: Optional[str] = Field(None, max_length=50)
    action: Optional[str] = Field(None, max_length=100)
    entity_name: Optional[str] = Field(None, max_length=50)
    entity_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

