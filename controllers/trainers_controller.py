from sqlalchemy.orm import Session
from models.trainer import Trainer
from schemas.trainer_schema import TrainerCreate, TrainerUpdate
from config.exceptions import NotFoundException, InvalidDataException


def create_trainer(db: Session, payload: TrainerCreate) -> Trainer:
    trainer = Trainer(
        user_id=payload.user_id,
        specialty=payload.specialty,
        is_active=True
    )

    db.add(trainer)
    db.commit()
    db.refresh(trainer)

    return trainer


def get_all_trainers(db: Session) -> list[Trainer]:
    return db.query(Trainer).all()


def get_trainer_by_id(db: Session, trainer_id: int) -> Trainer:
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    if not trainer:
        raise NotFoundException("Entrenador no encontrado")

    return trainer


def update_trainer_specialty(
    db: Session,
    trainer_id: int,
    payload: TrainerUpdate
) -> Trainer:
    trainer = get_trainer_by_id(db, trainer_id)

    if payload.specialty is not None:
        trainer.specialty = payload.specialty

    db.commit()
    db.refresh(trainer)

    return trainer


def set_trainer_active_status(
    db: Session,
    trainer_id: int,
    is_active: bool
) -> Trainer:
    trainer = get_trainer_by_id(db, trainer_id)

    if is_active and not trainer.user_id:
        raise InvalidDataException(
            "No es posible activar el entrenador si no tiene un usuario asociado"
        )

    trainer.is_active = is_active

    db.commit()
    db.refresh(trainer)

    return trainer


def delete_trainer(db: Session, trainer_id: int) -> Trainer:
    """
    Soft delete: deactivate trainer
    Rule: cannot delete trainer with active classes
    """
    trainer = get_trainer_by_id(db, trainer_id)

    has_active_classes = any(
        user_class.is_active for user_class in trainer.classes
    )

    if has_active_classes:
        raise InvalidDataException(
            "No se puede eliminar el entrenador porque tiene clases activas"
        )

    trainer.is_active = False

    db.commit()
    db.refresh(trainer)

    return trainer
