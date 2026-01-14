from fastapi import status

#Crear entrenador
def test_create_trainer(client):
    response = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Yoga"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data["specialty"] == "Yoga"
    assert data["is_active"] is True

#Obtener todos
def test_get_all_trainers(client):
    response = client.get("/trainers")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

#Obtener por ID
def test_get_trainer_by_id(client):
    create = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Pilates"
        }
    )

    trainer_id = create.json()["id"]

    response = client.get(f"/trainers/{trainer_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["specialty"] == "Pilates"

#Actualizar especialidad
def test_update_trainer_specialty(client):
    create = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Yoga"
        }
    )

    trainer_id = create.json()["id"]

    response = client.put(
        f"/trainers/{trainer_id}/specialty",
        json={"specialty": "Crossfit"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["specialty"] == "Crossfit"

#Activar / desactivar
def test_deactivate_trainer(client):
    create = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Yoga"
        }
    )

    trainer_id = create.json()["id"]

    response = client.patch(
        f"/trainers/{trainer_id}/active?is_active=false"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"] is False

#Eliminar (soft delete)
def test_delete_trainer(client):
    create = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Yoga"
        }
    )

    trainer_id = create.json()["id"]

    response = client.delete(f"/trainers/{trainer_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_active"] is False
