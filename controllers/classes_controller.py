from sqlalchemy.orm import Session
from models.gym_class import GymClass
from schemas.gym_class_schema import GymClassCreate, GymClassUpdate


def create_class(db: Session, class_data: GymClassCreate):
    gym_class = GymClass(
        name=class_data.name,
        description=class_data.description
    )
    db.add(gym_class)
    db.commit()
    db.refresh(gym_class)
    return gym_class


def get_classes(db: Session):
    return db.query(GymClass).filter(GymClass.is_active == True).all()


def get_class_by_id(db: Session, class_id: int):
    return db.query(GymClass).filter(
        GymClass.id == class_id,
        GymClass.is_active == True
    ).first()


def update_class(db: Session, class_id: int, class_data: GymClassUpdate):
    gym_class = get_class_by_id(db, class_id)
    if not gym_class:
        return None


    if class_data.name is not None:
        gym_class.name = class_data.name
    if class_data.description is not None:
        gym_class.description = class_data.description


    db.commit()
    db.refresh(gym_class)
    return gym_class


def delete_class(db: Session, class_id: int):
    gym_class = get_class_by_id(db, class_id)
    if not gym_class:
        return None


    # Borrado lógico
    gym_class.is_active = False
    db.commit()
    db.refresh(gym_class)
    return gym_class
