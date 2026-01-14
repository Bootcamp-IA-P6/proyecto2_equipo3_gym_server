import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.gym_class_schema import GymClassCreate, GymClassUpdate, GymClassResponse

# ================================
# Tests para GymClassCreate
# ================================

def test_gymclass_create_valid():
    """Test de creación válida"""
    data = GymClassCreate(name="Yoga", description="Clase de relajación")
    assert data.name == "Yoga"
    assert data.description == "Clase de relajación"

def test_gymclass_create_only_name():
    """Test de creación con solo el campo obligatorio"""
    data = GymClassCreate(name="Pilates")
    assert data.name == "Pilates"
    assert data.description is None

def test_gymclass_create_invalid():
    """Test de creación inválida: falta el campo 'name'"""
    with pytest.raises(ValidationError):
        GymClassCreate(description="Clase sin nombre")

# ================================
# Tests para GymClassUpdate
# ================================

def test_gymclass_update_name_only():
    """Actualizar solo el nombre"""
    update = GymClassUpdate(name="Zumba")
    assert update.name == "Zumba"
    assert update.description is None

def test_gymclass_update_description_only():
    """Actualizar solo la descripción"""
    update = GymClassUpdate(description="Clase divertida")
    assert update.name is None
    assert update.description == "Clase divertida"

def test_gymclass_update_both():
    """Actualizar nombre y descripción"""
    update = GymClassUpdate(name="CrossFit", description="Clase intensa")
    assert update.name == "CrossFit"
    assert update.description == "Clase intensa"

# ================================
# Tests para GymClassResponse
# ================================

def test_gymclass_response_valid():
    """Test de respuesta completa"""
    now = datetime.now()
    response = GymClassResponse(
        id=1,
        name="HIIT",
        description="Entrenamiento intenso",
        is_active=True,
        created_at=now
    )
    assert response.id == 1
    assert response.name == "HIIT"
    assert response.description == "Entrenamiento intenso"
    assert response.is_active is True
    assert isinstance(response.created_at, datetime)
