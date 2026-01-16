from sqlalchemy.orm import Session
from models.trainer import Trainer
from models.user_class import UserClass
from models.gym_class import GymClass
from config.logger import get_logger
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


logger = get_logger(__name__)


def delete_trainer(db: Session, trainer_id: int) -> Trainer | None:
    """
    Soft delete trainer.
    Regla: No se puede desactivar si tiene clases activas en el sistema.
    """
    # 1. Buscamos al entrenador primero
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    if not trainer:
        logger.error(f"Intento de eliminar entrenador inexistente con ID: {trainer_id}")
        return None

    # 2. 🔍 REGLA DE NEGOCIO MEJORADA
    # Verificamos si este ID de entrenador aparece en CUALQUIER inscripción 
    # vinculada a una clase que esté marcada como 'is_active = True'
    active_enrollments_count = (
        db.query(UserClass)
        .join(GymClass, GymClass.id == UserClass.class_id)
        .filter(
            UserClass.trainer_id == trainer.id, # Usamos el ID real del objeto encontrado
            GymClass.is_active == True
        )
        .count()
    )

    # Log para depuración (esto te saldrá en la terminal del VSCode)
    logger.debug(f"Verificando entrenador {trainer_id}: Clases activas encontradas = {active_enrollments_count}")

    if active_enrollments_count > 0:
        logger.warning(
            f"Bloqueado: El Entrenador {trainer_id} tiene {active_enrollments_count} inscripciones activas."
        )
        raise InvalidDataException(
            "No se puede desactivar el entrenador porque tiene clases activas asignadas."
        )

    # 3. Si llegamos aquí, es que no tiene clases activas
    logger.info(f"Desactivando entrenador {trainer_id} (Soft Delete exitoso)")
    trainer.is_active = False
    
    db.commit()
    db.refresh(trainer)

    return trainer