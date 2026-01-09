from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("admin", "trainer", "user", name="user_roles"),
        nullable=False
    )
    

    trainer = relationship(
        "Trainer",
        back_populates="user",
        uselist=False
    )

    enrollments = relationship(
        "UserClass",
        back_populates="user"
    )
