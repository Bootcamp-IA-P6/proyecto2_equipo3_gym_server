from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base, TimestampMixin

class GymClass(Base, TimestampMixin):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    users = relationship(
        "UserClass",
        back_populates="gym_class"
    )
