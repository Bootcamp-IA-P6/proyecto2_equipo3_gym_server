from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate
from config.exceptions import NotFoundException, InvalidDataException


def create_user(db: Session, user_data: UserCreate):
    # Comprobar si el email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise InvalidDataException("El email ya está registrado")

    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=user_data.password,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session):
    """
    Devuelve todos los usuarios activos.
    """
    return db.query(User).filter(User.is_active == True).all()


def get_user_by_id(db: Session, user_id: int):
    """
    Devuelve un usuario por su ID.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise NotFoundException("Usuario no encontrado")

    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """
    Actualiza los datos de un usuario.
    """
    user = get_user_by_id(db, user_id)

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def activate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """
    Desactiva un usuario (borrado lógico).
    """
    user = get_user_by_id(db, user_id)

    user.is_active = False
    db.commit()
    db.refresh(user)

    return {"message": "Usuario desactivado correctamente"}
