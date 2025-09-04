from fastapi.testclient import TestClient
from app.main import app
from app.utils.jwt_handler import create_jwt
import os
from dotenv import load_dotenv

# Cargar .env si no está en entorno (útil para entorno local)
if not os.getenv("API_KEY") or not os.getenv("SECRET_KEY"):
    load_dotenv()

client = TestClient(app)

def test_valid_post():
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")  # Cargar la variable SECRET_KEY
    jwt_token = create_jwt({"user": "test"}, secret_key=SECRET_KEY, expires_in=60)  # Pasar SECRET_KEY como argumento

    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }

    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": API_KEY,
            "X-JWT-KWY": jwt_token
        },
        json=payload
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Hello Juan Perez your message will be send"

def test_missing_api_key():
    SECRET_KEY = os.getenv("SECRET_KEY")  # Cargar la variable SECRET_KEY
    jwt_token = create_jwt({"user": "test"}, secret_key=SECRET_KEY, expires_in=604800)  # Pasar SECRET_KEY como argumento

    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }

    response = client.post(
        "/DevOps",
        headers={
            "X-JWT-KWY": jwt_token
        },
        json=payload
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API Key"

def test_invalid_jwt():
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")  # Cargar la variable SECRET_KEY
    payload = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }

    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": API_KEY,
            "X-JWT-KWY": "invalid.token.value"
        },
        json=payload
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid or missing JWT"

def test_invalid_method_get():
    response = client.get("/DevOps")
    assert response.status_code == 200
    assert response.text == '"ERROR"'

def test_generate_jwt():
    response = client.get("/generate-jwt")
    assert response.status_code == 200
    assert "jwt" in response.json()
