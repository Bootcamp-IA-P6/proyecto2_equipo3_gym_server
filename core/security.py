import bcrypt

def hash_password(password: str) -> str:
    """
    Recibe una contraseña en texto plano
    y devuelve un hash seguro.
    """
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Comprueba si una contraseña coincide con su hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
