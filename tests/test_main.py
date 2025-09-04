import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.main import app
from app.utils.jwt_handler import create_jwt

# Cargar .env si faltan variables (solo útil en local)
if not os.getenv("API_KEY") or not os.getenv("SECRET_KEY"):
    load_dotenv()

client = TestClient(app)


def _payload() -> dict:
    return {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45,
    }


def test_valid_post():
    api_key = os.getenv("API_KEY")
    secret_key = os.getenv("SECRET_KEY")
    assert api_key and secret_key, "API_KEY/SECRET_KEY no están definidos"

    jwt_token = create_jwt(
        {"user": "test"},
        secret_key=secret_key,
        expires_in=60,
    )

    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": api_key,
            "X-JWT-KWY": jwt_token,
        },
        json=_payload(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Hello Juan Perez your message will be send"
    )


def test_missing_api_key():
    secret_key = os.getenv("SECRET_KEY")
    assert secret_key, "SECRET_KEY no está definido"

    jwt_token = create_jwt(
        {"user": "test"},
        secret_key=secret_key,
        expires_in=604800,
    )

    response = client.post(
        "/DevOps",
        headers={"X-JWT-KWY": jwt_token},
        json=_payload(),
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or missing API Key"


def test_invalid_jwt():
    api_key = os.getenv("API_KEY")
    assert api_key, "API_KEY no está definido"

    response = client.post(
        "/DevOps",
        headers={
            "X-Parse-REST-API-Key": api_key,
            "X-JWT-KWY": "invalid.token.value",
        },
        json=_payload(),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid or missing JWT"


def test_invalid_method_get():
    response = client.get("/DevOps")
    assert response.status_code == 200
    # FastAPI devuelve un JSON string, por eso las comillas en el body:
    assert response.text == '"ERROR"'


def test_generate_jwt():
    response = client.get("/generate-jwt")
    assert response.status_code == 200
    assert "jwt" in response.json()
