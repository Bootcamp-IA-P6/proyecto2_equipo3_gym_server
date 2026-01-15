from fastapi import status
import pytest

# Los fixtures se pueden definir aquí o en conftest.py
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)


# Errores de creación
def test_create_trainer_missing_specialty(client):
    response = client.post("/trainers", json={"user_id": 1})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_trainer_missing_user_id(client):
    response = client.post("/trainers", json={"specialty": "Yoga"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Not found
def test_get_trainer_not_found(client):
    response = client.get("/trainers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Entrenador no encontrado"

# Update inexistente
def test_update_trainer_not_found(client):
    response = client.put("/trainers/999/specialty", json={"specialty": "Pilates"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Entrenador no encontrado"

# Delete inexistente
def test_delete_trainer_not_found(client):
    response = client.delete("/trainers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Entrenador no encontrado"
