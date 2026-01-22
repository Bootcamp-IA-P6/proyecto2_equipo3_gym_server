from pydantic import BaseModel
from typing import Optional


class TrainerBase(BaseModel):
    specialty: str


class TrainerCreate(TrainerBase):
    user_id: int


class TrainerUpdate(BaseModel):
    specialty: Optional[str] = None


class TrainerResponse(TrainerBase):
    id: int
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True
