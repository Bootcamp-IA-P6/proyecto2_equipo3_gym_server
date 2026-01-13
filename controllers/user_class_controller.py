from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_class import UserClass
from schemas.user_class_schema import UserClassCreate

from models.user import User
from models.trainer import Trainer


def get_all_users_classes(db: Session):
    """
    Devuelve todos los usuarios, clases y profesores.
    """
    users = db.query(UserClass).all()
    return users

def create_user_class(db: Session, user_class_data: UserClassCreate):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    # Comprobar si el usuario ya existe
    existing_user = db.query(User).filter(User.id == user_class_data.id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    # Hacer lo mismo con el id de la clase y el id del trainer
    # Comprobar si la inscripcion ya existe.

    new_user_class = UserClass(
        user_id=user_class_data.user_id,
        class_id=user_class_data.class_id,
        trainer_id=user_class_data.trainer_id,
    )

    db.add(new_user_class)
    db.commit()
    db.refresh(new_user_class)

    return new_user_class

def get_classes_by_userid(db: Session, user_id: int):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user_classes = db.query(UserClass).filter(UserClass.user_id == user_id).all()

    return user_classes

# Cuando suban elcontrolador de las clases
def get_users_by_classid(db: Session, class_id: int):
    """
    Devuelve las clases a las que está apuntado un usuario.
    """
    # user = db.query(User).filter(User.id == user_id).first()

    # if not user:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Usuario no encontrado"
    #     )

    class_users = db.query(UserClass).filter(UserClass.class_id == class_id).all()
    
    return class_users


def delete_inscription(db: Session, user_id: int):
    """
    Borra un usuario y todas sus clases a las que esta inscrito.
    """
    rows = db.query(UserClass).filter(UserClass.user_id == user_id).delete()

    if rows:
        db.commit()
        return {"message": "inscripcion borrada correctamente"}
    
    return {"message": "El usuario no está inscrito a ninguna clase"}