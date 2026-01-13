from sqlalchemy.orm import Session
from models.trainer import Trainer
from schemas.trainer_schema import TrainerCreate, TrainerUpdate

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

def get_trainer_by_id(db: Session, trainer_id: int) -> Trainer | None:
    return db.query(Trainer).filter(Trainer.id == trainer_id).first()

def update_trainer_specialty( db: Session, trainer_id: int, payload: TrainerUpdate) -> Trainer | None:
    trainer = get_trainer_by_id(db, trainer_id)
    if not trainer:
        return None
    if payload.specialty is not None:
        trainer.specialty = payload.specialty

    db.commit()
    db.refresh(trainer)

    return trainer

def set_trainer_active_status( db: Session, trainer_id: int, is_active: bool) -> Trainer | None:
    trainer = get_trainer_by_id(db, trainer_id)

    if not trainer:
        return None

     # No se puede activar un trainer sin usuario
    if is_active and not trainer.user_id:
        raise ValueError("No es posible activar el entrenador si no tiene un usuario asociado")
    
    trainer.is_active = is_active

    db.commit()
    db.refresh(trainer)

    return trainer

def delete_trainer(db: Session, trainer_id: int) -> Trainer | None:
    """
    Soft delete: deactivate trainer
    Rule: cannot delete trainer with active classes
    """
    trainer = get_trainer_by_id(db, trainer_id)

    if not trainer:
        return None

    # No se puede eliminar si tiene al menos una clase activa
    has_active_classes = any( user_class.is_active for user_class in trainer.classes)

    if has_active_classes:
        raise ValueError(
            "No se puede eliminar el entrenador porque tiene clases activas")

    trainer.is_active = False

    db.commit()
    db.refresh(trainer)

    return trainer
