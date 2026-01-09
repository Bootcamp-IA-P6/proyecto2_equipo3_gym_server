from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Boolean, DateTime, func

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())