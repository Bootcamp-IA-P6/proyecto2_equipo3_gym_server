from datetime import datetime, timedelta
from jose import jwt, JWTError
from config.settings import settings


def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = expires_minutes)
    to_encode.update({"exp": expire})
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
        
    )
    
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        return payload
    except JWTError:
        return None
     