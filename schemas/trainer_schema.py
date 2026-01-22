from pydantic import BaseModel
from typing import Optional

class UserInfo(BaseModel):
    name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


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
    user: Optional[UserInfo] = None

    class Config:
        from_attributes = True
