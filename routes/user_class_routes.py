from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from controllers import user_class_controller
from schemas.user_class_schema import UserClassCreate, UserClassResponse

router = APIRouter (
    prefix="/user_class",
    tags= {"User_Class"} #para Swagger (orden y nombre bonito)
)

@router.get("/", response_model=list[UserClassResponse])
def get_user_class(
    db: Session = Depends(get_db)
):
    return user_class_controller.get_all_users_classes(db)


@router.get("/clases/{user_id}", response_model=list[UserClassResponse])
def get_userId_classes(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_class_controller.get_classes_by_userid(db, user_id)


@router.post("/", response_model=UserClassResponse, status_code=status.HTTP_201_CREATED)
def create_user_class(
    user_class: UserClassCreate,
    db: Session = Depends(get_db)
    
):
     return user_class_controller.create_user_class(db, user_class)



# @router.delete("/{user_id}")
# def delete_user_class(
#     user_id: int,
#     db: Session = Depends(get_db)
# ):
#     return users_controller.delete_user(db, user_id)