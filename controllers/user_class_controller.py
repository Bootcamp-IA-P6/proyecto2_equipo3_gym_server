from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_class import UserClass
from schemas.user_class_schema import UserClassCreate

from models.user import User
from models.trainer import Trainer
from models.gym_class import GymClass
from config.logger import get_logger

logger = get_logger(__name__)

# def get_all_users_classes(db: Session):
#     """
#     Devuelve todos los usuarios, clases y profesores.
#     """
#     logger.debug("Consultando todas las inscripciones del sistema")
#     users = db.query(UserClass).all()
    
#     logger.info(f"Se han recuperado {len(users)} registros de inscripciones")
#     return users

# ---- Función get con filtros y paginación .....
def get_users_classes_with_filters(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    user_id: int = None, 
    class_id: int = None, 
    trainer_id: int = None
):
    """
    Devuelve las inscripciones con filtros por ID de usuario, clase o profesor, y paginación.
    """
    logger.debug(f"Consultando inscripciones -> skip: {skip}, limit: {limit}, user: {user_id}, class: {class_id}")
    
    # 1. La consulta base
    query = db.query(UserClass)

    # 2. Filtros
    if user_id:
        query = query.filter(UserClass.user_id == user_id)
    
    if class_id:
        query = query.filter(UserClass.class_id == class_id)
        
    if trainer_id:
        query = query.filter(UserClass.trainer_id == trainer_id)

    # 3. Paginación y ejecución
    enrollments = query.offset(skip).limit(limit).all()
    
    logger.info(f"Se han recuperado {len(enrollments)} registros de inscripciones")
    return enrollments
# ------------------------------------------------

def create_user_class(db: Session, user_class_data: UserClassCreate):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    logger.info(
        f"Intentando inscribir usuario {user_class_data.user_id} "
        f"en la clase {user_class_data.class_id} con el entrenador {user_class_data.trainer_id}"
    )

    # Comprobar si el usuario ya existe
    existing_user = db.query(User).filter(User.id == user_class_data.user_id).first()
    if not existing_user:
        logger.warning(f"Fallo de inscripción: El usuario {user_class_data.user_id} no existe")
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    # Comprobar si la clase existe
    existing_class = db.query(GymClass).filter(GymClass.id == user_class_data.class_id).first()
    if not existing_class:
        logger.warning(f"Fallo de inscripción: La clase {user_class_data.class_id} no existe")
        raise HTTPException(status_code=400, detail="La clase no existe")
    
    # Comprobar si el entrenador existe
    existing_trainer = db.query(Trainer).filter(Trainer.id == user_class_data.trainer_id).first()
    if not existing_trainer:
        logger.warning(f"Fallo de inscripción: El entrenador {user_class_data.trainer_id} no existe")
        raise HTTPException(status_code=400, detail="El entrenador no existe")
    
    # Comprobar si la inscripcion ya existe.
    existing_user_class = db.query(UserClass).filter(
        UserClass.user_id == user_class_data.user_id, 
        UserClass.class_id == user_class_data.class_id
        ).first()
    if existing_user_class:
        logger.warning(
            f"Fallo de inscripción: El usuario {user_class_data.user_id} "
            f"ya está en la clase {user_class_data.class_id}"
        )
        raise HTTPException(status_code=400, detail="El usuario ya está apuntado a esta clase")

    new_user_class = UserClass(
        user_id=user_class_data.user_id,
        class_id=user_class_data.class_id,
        trainer_id=user_class_data.trainer_id,
    )

    db.add(new_user_class)
    db.commit()
    db.refresh(new_user_class)

    logger.info(f"Inscripción creada con éxito: Usuario {new_user_class.user_id} -> Clase {new_user_class.class_id}")
    return new_user_class


def get_classes_by_userid(db: Session, user_id: int):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    logger.debug(f"Buscando clases para el usuario ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user_classes = db.query(UserClass).filter(UserClass.user_id == user_id).all()

    logger.info(f"Usuario {user_id} tiene {len(user_classes)} clases inscritas")
    return user_classes


def get_users_by_classid(db: Session, class_id: int):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    logger.debug(f"Buscando alumnos para la clase ID: {class_id}")
    gymclass = db.query(GymClass).filter(GymClass.id == class_id).first()

    if not gymclass:
        raise HTTPException(
            status_code=404,
            detail="Clase no encontrada"
        )

    class_users = db.query(UserClass).filter(UserClass.class_id == class_id).all()
    
    logger.info(f"La clase {class_id} tiene {len(class_users)} alumnos inscritos")
    return class_users


def delete_inscription(db: Session, user_id: int):
    """
    Borra un usuario y todas sus clases a las que esta inscrito.
    """
    logger.info(f"Borrando todas las inscripciones del usuario ID: {user_id}")
    
    rows = db.query(UserClass).filter(UserClass.user_id == user_id).delete()

    if rows:
        db.commit()
        logger.info(f"Se han eliminado {rows} inscripciones para el usuario {user_id}")
        return {"message": "inscripcion borrada correctamente"}
    
    logger.warning(f"Intento de borrar inscripciones: El usuario {user_id} no tenía ninguna")
    return {"message": "El usuario no está inscrito a ninguna clase"}


def delete_user_class(db: Session, user_id: int, class_id: int):
    """
    Borra un usuario y de una clase a la que esta inscrito.
    """
    logger.info(f"Eliminando usuario {user_id} de la clase {class_id}")
    
    row = db.query(UserClass).filter(
        UserClass.user_id == user_id, 
        UserClass.class_id == class_id).delete()

    if row:
        db.commit()
        logger.info(f"Usuario {user_id} eliminado de la clase {class_id}")
        return {"message": "Usuario borrado de esta clase correctamente"}

    logger.warning(f"Fallo al borrar: El usuario {user_id} no estaba en la clase {class_id}")
    return {"message": "El usuario no está inscrito a esta clase"}