from pydantic import BaseModel


class UserClassCreate(BaseModel):
    user_id: int
    class_id: int
    trainer_id: int


class UserClassResponse(BaseModel):
    id: int
    user_id: int
    class_id: int
    trainer_id: int

    class Config:
        from_attributes = True
