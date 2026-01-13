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
