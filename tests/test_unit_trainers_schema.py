import pytest
from pydantic import ValidationError

from schemas.trainer_schema import (
    TrainerBase,
    TrainerCreate,
    TrainerUpdate,
    TrainerResponse
)

#TrainerBase
def test_trainer_base_valid():
    schema = TrainerBase(specialty="Yoga")
    assert schema.specialty == "Yoga"

def test_trainer_base_missing_specialty():
    with pytest.raises(ValidationError):
        TrainerBase()

#TrainerCreate
def test_trainer_create_valid():
    schema = TrainerCreate(
        user_id=1,
        specialty="Pilates"
    )

    assert schema.user_id == 1
    assert schema.specialty == "Pilates"


def test_trainer_create_missing_user_id():
    with pytest.raises(ValidationError):
        TrainerCreate(specialty="Yoga")


def test_trainer_create_missing_specialty():
    with pytest.raises(ValidationError):
        TrainerCreate(user_id=1)

#TrainerUpdate
def test_trainer_update_empty():
    schema = TrainerUpdate()
    assert schema.specialty is None


def test_trainer_update_with_specialty():
    schema = TrainerUpdate(specialty="Crossfit")
    assert schema.specialty == "Crossfit"

#TrainerResponse + from_attributes
class FakeTrainer:
    def __init__(self):
        self.id = 1
        self.user_id = 10
        self.specialty = "Pilates"
        self.is_active = True


def test_trainer_response_valid():
    schema = TrainerResponse(
        id=1,
        user_id=2,
        specialty="Yoga",
        is_active=True
    )

    assert schema.id == 1
    assert schema.user_id == 2
    assert schema.specialty == "Yoga"
    assert schema.is_active is True


def test_trainer_response_from_attributes():
    fake_trainer = FakeTrainer()

    schema = TrainerResponse.model_validate(fake_trainer)

    assert schema.id == 1
    assert schema.user_id == 10
    assert schema.specialty == "Pilates"
    assert schema.is_active is True
