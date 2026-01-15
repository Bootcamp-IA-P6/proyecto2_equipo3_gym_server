from fastapi import status

# Test de integración que necesita primero tener creado un usuario, una clase y un entrenador.
#Crear el usuario
def test_create_user_juan(client):
    response = client.post(
        "/users",
        json={
            "name": "Ana",
            "last_name": "García",
            "email": "ana@test.com",
            "password": "123456",
            "role": "user"
        }
    )
    
    assert response.status_code == 200

#Crear entrenador
def test_create_trainer_juan(client):
    response = client.post(
        "/trainers",
        json={
            "user_id": 1,
            "specialty": "Yoga"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

#Crear la clase
def test_create_class_juan(client, name="Yoga", description="Clase"):
    response = client.post(
        "/gym-classes",
        json={"name": name, "description": description}
    )
    assert response.status_code == 200


def test_create_user_class_juan(client):
    response = client.post(
        "/user_class",
        json={
            "user_id": 1,
            "class_id": 1,
            "trainer_id": 1
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["user_id"] == 1
    assert data["trainer_id"] == 1

# FIN Test de integración que necesita primero tener creado un usuario, una clase y un entrenador.

# Tests de integración 
def test_get(client):
    response = client.get("/user_class")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_user_by_user_id(client):
    response = client.get("/user_class/user_classes/1")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_user_by_class_id(client):
    response = client.get("/user_class/class_users/1")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

