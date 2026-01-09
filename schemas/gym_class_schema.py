from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GymClassBase(BaseModel):
    name: str
    description: Optional[str] = None


class GymClassCreate(GymClassBase):
    pass


class GymClassUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GymClassResponse(GymClassBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
