from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from core.security import verify_password
from core.jwt import create_access_token
from config.logger import get_logger

logger = get_logger(__name__)

def login_user(db: Session, email: str, password: str):
    """
    Autentica un usuario y devuelve un JWT.
    """
    logger.info(f"Intento de inicio de sesión para el email: {email}")

    user = db.query(User).filter(User.email == email).first()
    
    # Caso: Usuario no existe o está desactivado
    if not user:
        logger.warning(f"Fallo de login: No existe usuario con email {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
        
    if not user.is_active:
        logger.warning(f"Fallo de login: El usuario {email} está desactivado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    if not verify_password(password, user.password_hash):
        logger.warning(f"Fallo de login: Contraseña incorrecta para el usuario {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    logger.debug(f"Generando token de acceso para el usuario ID: {user.id}")
    token = create_access_token(
        data={
            "user_id": user.id,
            "role": user.role
        }
    )

    logger.info(f"Login exitoso: Usuario {user.id} ha iniciado sesión con rol '{user.role}'")
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
