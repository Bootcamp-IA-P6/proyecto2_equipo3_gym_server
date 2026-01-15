from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from database import get_db
from controllers.classes_controller import (
    create_class,
    get_classes,
    get_class_by_id,
    update_class,
    delete_class
)
from schemas.gym_class_schema import GymClassCreate, GymClassUpdate, GymClassResponse
from config.exceptions import AppException, NotFoundException,InvalidDataException # Colocar clases 
#cuando se suban los tests que faltan 


router = APIRouter(
    prefix="/gym-classes",
    tags=["Gym Classes"]
)


@router.post("/", response_model=GymClassResponse)
def create(gym_class: GymClassCreate, db: Session = Depends(get_db)):
    return create_class(db, gym_class)


@router.get("/", response_model=List[GymClassResponse])
def list_classes(db: Session = Depends(get_db)):
    return get_classes(db)


@router.get("/{class_id}", response_model=GymClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    gym_class = get_class_by_id(db, class_id)
    if not gym_class:
        #raise HTTPException(status_code=404, detail="Class not found")
        raise NotFoundException("Clase no encontrada")  # <-- Handler centralizado
    return gym_class


@router.put("/{class_id}", response_model=GymClassResponse)
def update(class_id: int, class_data: GymClassUpdate, db: Session = Depends(get_db)):
    gym_class = update_class(db, class_id, class_data)
    if not gym_class:
        #raise HTTPException(status_code=404, detail="Class not found")
        raise NotFoundException("Clase no encontrada")  # <-- Handler centralizado
    return gym_class


@router.delete("/{class_id}", response_model=GymClassResponse)
def delete(class_id: int, db: Session = Depends(get_db)):
    gym_class = delete_class(db, class_id)
    if not gym_class:
        #raise HTTPException(status_code=404, detail="Class not found")
        raise NotFoundException("Clase no encontrada")  # <-- Handler centralizado
    return gym_class
