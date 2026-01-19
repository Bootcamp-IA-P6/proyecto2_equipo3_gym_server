import sys
import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Añade la raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models.base import Base
from database.database import get_db

# --- NUEVO IMPORT NECESARIO ---
from core.dependencies import get_current_user
# ------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- NUEVA FUNCIÓN DE OVERRIDE PARA AUTH ---
def override_get_current_user():
    # Devolvemos un objeto (diccionario) que simula el payload del token decodificado
    # Le damos rol "admin" para que pase todos los require_role(["admin", ...])
    return {
        "id": 1,
        "role": "admin", 
        "email": "test@admin.com",
        "is_active": True
    }
# -------------------------------------------

app.dependency_overrides[get_db] = override_get_db

# --- APLICAMOS EL OVERRIDE DE SEGURIDAD ---
app.dependency_overrides[get_current_user] = override_get_current_user
# ------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    # Nota: El override ya está aplicado globalmente arriba, 
    # así que el cliente lo usará automáticamente.
    return TestClient(app)