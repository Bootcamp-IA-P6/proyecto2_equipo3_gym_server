from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

class UserClass(Base):
    __tablename__ = "user_class"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)

    user = relationship(
        "User",
        back_populates="enrollments"
    )

    gym_class = relationship(
        "GymClass",
        back_populates="users"
    )

    trainer = relationship(
        "Trainer",
        back_populates="classes"
    )
