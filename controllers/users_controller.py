from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate
from core.security import hash_password

from config.exceptions import NotFoundException, InvalidDataException
from config.logger import get_logger

logger = get_logger(__name__)


def create_user(db: Session, user_data: UserCreate):
    logger.info(f"Intentando registrar nuevo usuario con email: {user_data.email}")

    # Comprobar si el email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        logger.warning(f"Registro fallido: El email {user_data.email} ya está en uso")
        raise InvalidDataException("El email ya está registrado")

    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"Usuario creado exitosamente. ID: {new_user.id}, Rol: {new_user.role}")
    return new_user


def get_all_users(db: Session):
    """
    Devuelve todos los usuarios activos.
    """
    logger.debug("Consultando lista de usuarios activos")
    users = db.query(User).filter(User.is_active == True).all()
    logger.info(f"Se han recuperado {len(users)} usuarios activos")
    return users

#---- La función get con filtos y paginacion ----
def get_users_with_filters(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    name: str = None, 
    role: str = None, 
    is_active: bool = True
):
    """
    Devuelve usuarios con filtros de nombre, rol y estado, además de paginación.
    """
    logger.debug(f"Consultando lista de usuarios con filtros -> skip: {skip}, limit: {limit}, name: {name}, role: {role}")
    
    # 1. Empezamos preparando la consulta (pero todavía no la enviamos a la base de datos)
    query = db.query(User)

    # 2. ¿El usuario quiere filtrar por nombre? Añadimos la regla
    if name:
        # Usamos ilike para que busque "ana" aunque en la BD ponga "Ana"
        query = query.filter(User.name.ilike(f"%{name}%"))
    
    # 3. ¿El usuario quiere filtrar por rol? Añadimos la regla
    if role:
        query = query.filter(User.role == role)
        
    # 4. Filtramos por estado (por defecto solo activos, pero se puede cambiar)
    query = query.filter(User.is_active == is_active)

    # 5. Aplicamos la paginación y ejecutamos la consulta con .all()
    users = query.offset(skip).limit(limit).all()
    
    logger.info(f"Se han recuperado {len(users)} usuarios tras aplicar filtros")
    return users
#----------------------------------------

def get_user_by_id(db: Session, user_id: int):
    """
    Devuelve un usuario por su ID.
    """
    logger.debug(f"Buscando detalles del usuario ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("Usuario no encontrado")

    return user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """
    Actualiza los datos de un usuario.
    """
    logger.info(f"Iniciando actualización para usuario ID: {user_id}")
    user = get_user_by_id(db, user_id)

    # Logueamos qué campos se están intentando cambiar
    update_data = user_data.dict(exclude_unset=True)
    logger.debug(f"Campos a actualizar para user {user_id}: {list(update_data.keys())}")

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    logger.info(f"Usuario {user_id} actualizado correctamente")
    return user


def activate_user(db: Session, user_id: int):
    logger.info(f"Activando cuenta del usuario ID: {user_id}")
    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)

    logger.info(f"Usuario {user_id} ahora está activo")
    return user


def delete_user(db: Session, user_id: int):
    """
    Desactiva un usuario (borrado lógico).
    """
    logger.info(f"Solicitud de desactivación para usuario ID: {user_id}")
    user = get_user_by_id(db, user_id)

    user.is_active = False
    db.commit()
    db.refresh(user)

    logger.info(f"Usuario {user_id} desactivado correctamente")
    return {"message": "Usuario desactivado correctamente"}
