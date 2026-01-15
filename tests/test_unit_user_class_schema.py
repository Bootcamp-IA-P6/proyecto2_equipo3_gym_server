import pytest
from schemas.user_class_schema import UserClassCreate, UserClassResponse
from pydantic import ValidationError

#Crear una UserClassCreate valida
def test_user_class_create_schema_valid():
    user_class = UserClassCreate(
        user_id=1,
        class_id=2,
        trainer_id=3
    )
    
    assert user_class.user_id == 1
    assert user_class.class_id == 2
    assert user_class.trainer_id == 3


#Poner una clase_id erronea en UserClassCreate y debe fallar
def test_user_class_create_schema_invalid_class_id():
    with pytest.raises(ValidationError):
        UserClassCreate(
            user_id=1,
            class_id="Yoga",
            trainer_id=3
        )


#Crear una UserClassResponse valida
def test_user_class_response_valid():
    user_class = UserClassResponse(
        id=1,
        user_id=1,
        class_id=2,
        trainer_id=3
    )
    
    assert user_class.id == 1
    assert user_class.user_id == 1
    assert user_class.class_id == 2
    assert user_class.trainer_id == 3