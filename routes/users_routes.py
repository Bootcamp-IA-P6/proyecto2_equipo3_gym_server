from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from controllers import users_controller
from schemas.user_schema import UserCreate, UserUpdate, UserResponse


router = APIRouter (
    prefix="/users",
    tags= {"Users"} #para Swagger (orden y nombre bonito)
)

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
    
):
     return users_controller.create_user(db, user)
 
@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return users_controller.get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return users_controller.get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return users_controller.update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return users_controller.delete_user(db, user_id)

@router.patch("/{user_id}/activate", response_model=UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    return users_controller.activate_user(db, user_id)
