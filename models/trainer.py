from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base, TimestampMixin

class Trainer(Base, TimestampMixin):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    specialty = Column(String(100), nullable=False)

    user = relationship(
        "User",
        back_populates="trainer"
    )

    classes = relationship(
        "UserClass",
        back_populates="trainer"
    )
