def test_create_user(client):
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

    data = response.json()
    assert data["email"] == "ana@test.com"
    assert data["is_active"] is True
    
def test_get_all_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_get_user_by_id(client):
    response = client.get("users/1")
    
    assert response.status_code == 200
    data= response.json()
    assert data["id"] == 1
    
def test_update_user(client):
    response = client.put(
        "/users/1",
        json= {
            "name": "Ana Maria"
        }
    )
    
    assert response.status_code == 200
    assert response.json()["name"] == "Ana Maria"
    
def test_delete_user(client):
    response = client.delete("/users/1")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario desactivado correctamente"

