import jwt
import os
from datetime import datetime, timedelta

# Conjunto para guardar los tokens usados
used_tokens = set()

def create_jwt(payload: dict, secret_key: str, expires_in: int = 60) -> str:
    if not secret_key:
        raise ValueError("SECRET_KEY no está definido. Verifica las variables de entorno en Azure.")
    
    payload.update({"exp": datetime.utcnow() + timedelta(seconds=expires_in)})
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def verify_jwt(token: str) -> bool:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY no está definido. Verifica las variables de entorno en Azure.")

    # Verificar si ya fue usado
    if token in used_tokens:
        return False  # Rechazado: token ya fue usado

    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
        used_tokens.add(token)  # Marcarlo como usado
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
