from sqlalchemy.orm import Session
from models.gym_class import GymClass
from schemas.gym_class_schema import GymClassCreate, GymClassUpdate
from config.exceptions import NotFoundException
from config.logger import get_logger

logger = get_logger(__name__)

def create_class(db: Session, class_data: GymClassCreate):
    logger.info(f"Intentando crear nueva clase: '{class_data.name}'")
   
    gym_class = GymClass(
        name=class_data.name,
        description=class_data.description
    )
    db.add(gym_class)
    db.commit()
    db.refresh(gym_class)

    logger.info(f"Clase creada exitosamente con ID: {gym_class.id}")
    return gym_class


def get_classes(db: Session):
    logger.debug("Consultando todas las clases activas")
    classes = db.query(GymClass).filter(GymClass.is_active == True).all()
    logger.info(f"Se han recuperado {len(classes)} clases activas")
    return classes

def get_class_by_id(db: Session, class_id: int):
    logger.debug(f"Buscando clase con ID: {class_id}")
    gym_class = db.query(GymClass).filter(
        GymClass.id == class_id,
        GymClass.is_active == True
    ).first()

    if not gym_class:
        raise NotFoundException("Clase no encontrada")

    return gym_class


def update_class(db: Session, class_id: int, class_data: GymClassUpdate):
    logger.info(f"Iniciando actualización de la clase ID: {class_id}")
    gym_class = get_class_by_id(db, class_id)

    if class_data.name is not None:
        logger.info(f"Cambiando nombre: '{gym_class.name}' -> '{class_data.name}'")
        gym_class.name = class_data.name
    
    if class_data.description is not None:
        gym_class.description = class_data.description
        logger.debug(f"Descripción actualizada para la clase {class_id}")

    db.commit()
    db.refresh(gym_class)
    logger.info(f"Clase {class_id} actualizada correctamente")
    return gym_class


def delete_class(db: Session, class_id: int):
    logger.info(f"Solicitud de desactivación para clase ID: {class_id}")
    gym_class = get_class_by_id(db, class_id)

    gym_class.is_active = False
    db.commit()
    db.refresh(gym_class)

    logger.info(f"Clase {class_id} marcada como inactiva.")
    return gym_class
