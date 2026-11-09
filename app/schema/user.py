from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schema.role import RoleResponse

class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    first_name: str = Field("", max_length=50)
    last_name: str = Field("", max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)
    role_ids: Optional[List[int]] = Field(default_factory=list)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    role_ids: Optional[List[int]] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    roles: List[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)

