from sqlalchemy.orm import Session
from models.trainer import Trainer
from models.user_class import UserClass
from models.gym_class import GymClass
from config.logger import get_logger
from schemas.trainer_schema import TrainerCreate, TrainerUpdate
from config.exceptions import NotFoundException, InvalidDataException

logger = get_logger(__name__)

def create_trainer(db: Session, payload: TrainerCreate) -> Trainer:
    logger.info(f"Creando nuevo entrenador para el usuario ID: {payload.user_id}")
    trainer = Trainer(
        user_id=payload.user_id,
        specialty=payload.specialty,
        is_active=True
    )

    db.add(trainer)
    db.commit()
    db.refresh(trainer)

    logger.info(f"Entrenador creado exitosamente con ID: {trainer.id}")
    return trainer


# def get_all_trainers(db: Session) -> list[Trainer]:
#     logger.debug("Consultando la lista completa de entrenadores")
#     trainers = db.query(Trainer).all()
#     logger.info(f"Se han recuperado {len(trainers)} entrenadores")
#     return trainers

# ---- la función get con filtros y paginación ----
def get_trainers_with_filters(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    specialty: str = None, 
    is_active: bool = True
) -> list[Trainer]:
    """
    Lista entrenadores con paginación y filtros por especialidad y estado.
    """
    logger.debug(f"Consultando entrenadores -> skip: {skip}, limit: {limit}, especialidad: {specialty}")
    
    # 1. Iniciamos la consulta base
    query = db.query(Trainer)

    # 2. Filtro por especialidad (si el usuario lo pide)
    if specialty:
        # Buscamos coincidencias parciales (ej: 'yoga' encontrará 'Yoga Integral')
        query = query.filter(Trainer.specialty.ilike(f"%{specialty}%"))
    
    # 3. Filtro por estado activo/inactivo
    if is_active is not None:
        query = query.filter(Trainer.is_active == is_active)

    # 4. Aplicamos el 'salto' (skip) y el 'límite' (limit)
    trainers = query.offset(skip).limit(limit).all()
    
    logger.info(f"Se han recuperado {len(trainers)} entrenadores con los filtros aplicados")
    return trainers
#------------------------------------------

def get_trainer_by_id(db: Session, trainer_id: int) -> Trainer:
    logger.debug(f"Buscando entrenador con ID: {trainer_id}")
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    if not trainer:
        # No ponemos logger.error aquí porque la excepción ya se captura en app.py
        raise NotFoundException("Entrenador no encontrado")

    return trainer


def update_trainer_specialty(db: Session, trainer_id: int, payload: TrainerUpdate) -> Trainer:
    logger.info(f"Actualizando especialidad del entrenador ID: {trainer_id}")
    trainer = get_trainer_by_id(db, trainer_id)

    if payload.specialty is not None:
        old_specialty = trainer.specialty
        trainer.specialty = payload.specialty
        logger.info(f"Especialidad cambiada: '{old_specialty}' -> '{payload.specialty}'")
    
    db.commit()
    db.refresh(trainer)
    return trainer


def set_trainer_active_status(db: Session, trainer_id: int, is_active: bool) -> Trainer:
    status_str = "activar" if is_active else "desactivar"
    logger.info(f"Intentando {status_str} al entrenador ID: {trainer_id}")
   
    trainer = get_trainer_by_id(db, trainer_id)

    if is_active and not trainer.user_id:
        logger.warning(f"Fallo al activar: Entrenador {trainer_id} no tiene usuario asociado")
        raise InvalidDataException(
            "No es posible activar el entrenador si no tiene un usuario asociado"
        )

    trainer.is_active = is_active

    db.commit()
    db.refresh(trainer)

    logger.info(f"Estado del entrenador {trainer_id} cambiado a: {'Activo' if is_active else 'Inactivo'}")
    return trainer


def delete_trainer(db: Session, trainer_id: int) -> Trainer | None:
    """
    Soft delete trainer.
    Regla: No se puede desactivar si tiene clases activas en el sistema.
    """
    logger.info(f"Iniciando proceso de desactivación (Soft Delete) para entrenador ID: {trainer_id}")
    
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    if not trainer:
        logger.error(f"Error: Intento de eliminar entrenador inexistente con ID: {trainer_id}")
        return None

    #  Verificación de seguridad:
    #  Verificamos si este ID de entrenador aparece en CUALQUIER inscripción 
    #  vinculada a una clase que esté marcada como 'is_active = True'
    active_enrollments_count = (
        db.query(UserClass)
        .join(GymClass, GymClass.id == UserClass.class_id)
        .filter(
            UserClass.trainer_id == trainer.id, 
            GymClass.is_active == True
        )
        .count()
    )

    logger.debug(f"Verificando entrenador {trainer_id}: Clases activas encontradas = {active_enrollments_count}")

    if active_enrollments_count > 0:
        logger.warning(
            f"Acción bloqueada: Entrenador {trainer_id} tiene {active_enrollments_count} clases activas"
        )
        raise InvalidDataException(
            "No se puede desactivar el entrenador porque tiene clases activas asignadas."
        )

    # Si llegamos aquí, es que no tiene clases activas
    logger.info(f"Desactivando entrenador {trainer_id}")
    trainer.is_active = False
    
    db.commit()
    db.refresh(trainer)

    logger.info(f"Entrenador {trainer_id} desactivado correctamente")
    return trainer