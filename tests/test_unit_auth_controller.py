import pytest
from fastapi import HTTPException
from controllers.auth_controller import login_user
from models.user import User
from core.security import hash_password


# Helper para crear usuarios en la DB de test
def create_user_for_auth(db, email, password, role="user", is_active=True):
    user = User(
        name="Test",
        last_name="Auth",
        email=email,
        password_hash=hash_password(password), # Importante hashear la pass
        role=role,
        is_active=is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Tests de Login (Lógica del Controller)

def test_login_success(db):
    """Prueba un login exitoso con credenciales correctas"""
    email = "valid@test.com"
    password = "password123"
    create_user_for_auth(db, email, password)

    # Llamamos directamente al controlador
    response = login_user(db, email, password)

    assert "access_token" in response
    assert response["token_type"] == "bearer"
    assert response["role"] == "user"
    # Verificar que el token es un string no vacío
    assert isinstance(response["access_token"], str)
    assert len(response["access_token"]) > 0

def test_login_user_not_found(db):
    """Prueba login con un email que no existe en la base de datos"""
    with pytest.raises(HTTPException) as excinfo:
        login_user(db, "noexiste@test.com", "123456")
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciales incorrectas"

def test_login_wrong_password(db):
    """Prueba login con usuario existente pero contraseña incorrecta"""
    email = "wrongpass@test.com"
    password = "correctpassword"
    create_user_for_auth(db, email, password)

    with pytest.raises(HTTPException) as excinfo:
        login_user(db, email, "passIncorrecta")
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Credenciales incorrectas"

def test_login_inactive_user(db):
    """Prueba login con usuario desactivado (is_active=False)"""
    email = "inactive@test.com"
    password = "password123"
    # Creamos usuario desactivado
    create_user_for_auth(db, email, password, is_active=False)

    with pytest.raises(HTTPException) as excinfo:
        login_user(db, email, password)
    
    assert excinfo.value.status_code == 401
    # Según tu controlador, el mensaje es el mismo por seguridad
    assert excinfo.value.detail == "Credenciales incorrectas" 

def test_login_admin_role(db):
    """Verifica que el rol se devuelve correctamente en la respuesta"""
    email = "admin@test.com"
    password = "adminpass"
    create_user_for_auth(db, email, password, role="admin")

    response = login_user(db, email, password)

    assert response["role"] == "admin"