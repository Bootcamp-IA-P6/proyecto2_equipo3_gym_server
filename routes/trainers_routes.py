from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.trainer_schema import TrainerCreate, TrainerUpdate, TrainerResponse
from controllers import trainers_controller

router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"]
)

@router.post( "/", response_model=TrainerResponse, status_code=status.HTTP_201_CREATED)
def create_trainer(
    payload: TrainerCreate,
    db: Session = Depends(get_db)
):
    return trainers_controller.create_trainer(db, payload)

@router.get( "/", response_model=list[TrainerResponse])
def get_trainers(
    db: Session = Depends(get_db)
):
    return trainers_controller.get_all_trainers(db)

@router.get( "/{trainer_id}", response_model=TrainerResponse)
def get_trainer(
    trainer_id: int,
    db: Session = Depends(get_db)
):
    trainer = trainers_controller.get_trainer_by_id(db, trainer_id)

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")
    return trainer

@router.put( "/{trainer_id}/specialty", response_model=TrainerResponse)
def update_trainer_specialty(
    trainer_id: int,
    payload: TrainerUpdate,
    db: Session = Depends(get_db)
):
    trainer = trainers_controller.update_trainer_specialty( db, trainer_id, payload)

    if not trainer:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")
    return trainer

@router.patch( "/{trainer_id}/active", response_model=TrainerResponse)
def set_trainer_active_status(
    trainer_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):
    try:
        trainer = trainers_controller.set_trainer_active_status(db, trainer_id, is_active)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")
    return trainer

@router.delete( "/{trainer_id}", response_model=TrainerResponse)
def delete_trainer(
    trainer_id: int,
    db: Session = Depends(get_db)
):
    try:
        trainer = trainers_controller.delete_trainer(db, trainer_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entrenador no encontrado")

    return trainer

