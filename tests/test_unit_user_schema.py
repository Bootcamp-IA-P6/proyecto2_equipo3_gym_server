import pytest
from schemas.user_schema import UserRole, UserCreate
from pydantic import ValidationError

# Verificar que exiten los roles
def test_user_role_enum_values():
    assert UserRole.admin.value == "admin"
    assert UserRole.trainer.value == "trainer"
    assert UserRole.user.value == "user"
    
#Crear un usuario valido
def test_user_create_schema_valid():
    user= UserCreate(
         name="Ana",
        last_name="García",
        email="ana@gmail.com",
        password="123456",
        role=UserRole.trainer
    )
    
    assert user.name == "Ana"
    assert user.email == "ana@gmail.com"

#poner un email invalio y debe fallar  
def test_user_create_schema_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            name="Ana",
            last_name="García",
            email="esto-no-es-un-email",
            password="123456",
            role=UserRole.user
        )
#poner un rol invalido y dede de fallar
def test_user_create_schema_invalid_role():
    with pytest.raises(ValidationError):
        UserCreate(
            name="Ana",
            last_name="García",
            email="ana@gmail.com",
            password="123456",
            role="superadmin"
        )
