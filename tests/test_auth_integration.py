from fastapi import status

def test_login_integration_success(client):
    """
    Prueba el flujo completo: 
    1. Crear un usuario (como admin simulado).
    2. Loguearse con ese usuario y recibir un token.
    """
    # 1. Preparamos los datos del usuario
    email = "login_success@test.com"
    password = "securePassword123"
    
    user_payload = {
        "name": "Login",
        "last_name": "User",
        "email": email,
        "password": password,
        "role": "trainer" 
    }

    # Creamos el usuario en la DB usando la API (gracias al mock de admin en conftest)
    create_response = client.post("/users", json=user_payload)
    assert create_response.status_code == 200

    # 2. Intentamos hacer LOGIN con las credenciales correctas
    login_payload = {
        "email": email,
        "password": password
    }
    
    response = client.post("/auth/login", json=login_payload)

    # 3. Verificaciones
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verificamos que devuelve el token y el rol correcto
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "trainer"


def test_login_integration_invalid_credentials(client):
    """
    Prueba que el login falla si la contraseña es incorrecta.
    """
    # 1. Creamos usuario
    email = "wrong_pass@test.com"
    password = "correctPassword"
    
    client.post("/users", json={
        "name": "Test", "last_name": "User", 
        "email": email, "password": password, "role": "user"
    })

    # 2. Intentamos login con contraseña INCORRECTA
    response = client.post("/auth/login", json={
        "email": email,
        "password": "WRONG_PASSWORD_123"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Credenciales incorrectas"


def test_login_integration_user_not_found(client):
    """
    Prueba login con un email que no existe en el sistema.
    """
    response = client.post("/auth/login", json={
        "email": "ghost@example.com",
        "password": "anyPassword"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Credenciales incorrectas"