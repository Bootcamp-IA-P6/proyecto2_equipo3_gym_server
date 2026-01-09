from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from models.base import Base

engine = create_engine(
    settings.DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)