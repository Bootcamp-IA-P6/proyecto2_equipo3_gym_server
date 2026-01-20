from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from controllers import users_controller
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from core.dependencies import require_role


router = APIRouter (
    prefix="/users",
    tags= {"Users"} #para Swagger (orden y nombre bonito)
)

@router.post("/",dependencies=[Depends(require_role(["admin"]))], response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
    
):
     return users_controller.create_user(db, user)
 
@router.get("/", dependencies=[Depends(require_role(["admin"]))], response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return users_controller.get_all_users(db)

#---- La ruta para la función get con filtos y paginacion ----
@router.get("/", dependencies=[Depends(require_role(["admin"]))], response_model=list[UserResponse])
def get_users_with_filters(
    skip: int = 0, 
    limit: int = 10, 
    name: str = None, 
    role: str = None, 
    is_active: bool = True,
    db: Session = Depends(get_db)
):
    # Llamamos al controlador pasándole todos los nuevos parámetros
    return users_controller.get_all_users(
        db, skip=skip, limit=limit, name=name, role=role, is_active=is_active
    )
#--------------------------------------------------

@router.get("/{user_id}", dependencies=[Depends(require_role(["admin"]))], response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return users_controller.get_user_by_id(db, user_id)

@router.put("/{user_id}", dependencies=[Depends(require_role(["admin"]))], response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    return users_controller.update_user(db, user_id, user)

@router.delete("/{user_id}", dependencies=[Depends(require_role(["admin"]))])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return users_controller.delete_user(db, user_id)

@router.patch("/{user_id}/activate", dependencies=[Depends(require_role(["admin"]))], response_model=UserResponse)
def activate_user(user_id: int, db: Session = Depends(get_db)):
    return users_controller.activate_user(db, user_id)
