from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_class import UserClass
from schemas.user_class_schema import UserClassCreate

from models.user import User


def get_all_users_classes(db: Session):
    """
    Devuelve todos los usuarios, clases y profesores.
    """
    users = db.query(UserClass).all()
    return users

def create_user_class(db: Session, user_class_data: UserClassCreate):
    # 1️⃣ Comprobar si el usuario ya existe
    existing_user = db.query(User).filter(User.id == user_class_data.id).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="El usuario no existe")
    
    # Hacer lo mismo con el id de la clase y el id del trainer

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

    # El usuario existe pero no tiene clases, comprobarlo con len??
    user_classes = db.query(UserClass).filter(UserClass.user_id == user_id).all()
    #return user
    return user_classes

# Cuando suban elcontrolador de las clases
# def get_users_by_classid(db: Session, user_id: int):
#     """
#     Devuelve las clases a las que está apuntado un usuario.
#     """
#     user = db.query(User).filter(User.id == user_id).first()

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="Usuario no encontrado"
#         )

#     # La clase existe pero no tiene usuarios, comprobarlo con len??
#     user_classes = db.query(UserClass).filter(UserClass.user_id == user_id).all()
#     #return user
#     return user_classes


# def delete_inscription(db: Session, user_id: int):
#     """
#     Borra un usuario y todas sus clases a las que esta apuntado.
#     """
#     user = get_user_by_id(db, user_id)

#     Comprobar que el usuario existe y borrar
#     Instruccion de borrar
    # db_libro = db.query(Libro).filter(Libro.id == libro_id).first()
    # if db_libro:
    #     db.delete(db_libro).filter()
    # en sqlalchemy en python controller como borrar todos los registros de un id
    #     db.query(UserClass).filter_by(id=valor_id).delete()
    #     db.commit()

#     db.commit()

#     return {"message": "inscripcion borrada correctamente"}