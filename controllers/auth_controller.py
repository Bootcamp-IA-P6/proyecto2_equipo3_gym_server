from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from core.security import verify_password
from core.jwt import create_access_token

def login_user(db: Session, email: str, password: str):
    """
    Autentica un usuario y devuelve un JWT.
    """
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    token = create_access_token(
        data={
            "user_id": user.id,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
