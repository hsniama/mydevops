import os
from app.utils.jwt_handler import create_jwt
from dotenv import load_dotenv

load_dotenv()

# Cargar la clave desde el entorno
secret_key = os.getenv("SECRET_KEY")

# Validación por si falta la clave
if not secret_key:
    raise ValueError("SECRET_KEY no está definida en el entorno")

# Se crea un JWT temporal de válido por 7 días (604800 segundos)
token = create_jwt({"user": "test"}, secret_key=secret_key, expires_in=604800)
print("JWT generado:", token)
