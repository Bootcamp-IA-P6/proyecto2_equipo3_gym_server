import pytest
from fastapi.testclient import TestClient
from app import app  

@pytest.fixture
def client():
    return TestClient(app)



def create_class(client, name="Yoga", description="Clase"):
    response = client.post(
        "/gym-classes",
        json={"name": name, "description": description}
    )
    assert response.status_code == 200
    return response.json()


def test_create_gym_class(client):
    data = create_class(client)
    assert data["name"] == "Yoga"
    assert data["is_active"] is True


def test_get_gym_classes(client):
    create_class(client, "Pilates", "Stretch")
    response = client.get("/gym-classes")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_gym_class_by_id(client):
    data = create_class(client, "Zumba", "Fun")
    response = client.get(f"/gym-classes/{data['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Zumba"


def test_update_gym_class(client):
    data = create_class(client, "CrossFit", "Intense")
    response = client.put(
        f"/gym-classes/{data['id']}",
        json={"name": "CrossFit Pro"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "CrossFit Pro"


def test_delete_gym_class(client):
    data = create_class(client, "HIIT", "Intense")
    response = client.delete(f"/gym-classes/{data['id']}")
    assert response.status_code == 200
    assert response.json()["is_active"] is False
