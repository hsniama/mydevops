import os

# --- Definir variables de entorno ANTES de importar app ---
os.environ.setdefault("API_KEY", "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c")
os.environ.setdefault("SECRET_KEY", "clave_super_secreta_de_tests")

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402
from app.utils.jwt_handler import create_jwt  # noqa: E402


client = TestClient(app)


def _payload() -> dict:
    return {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45,
    }


def test_valid_post():
    api_key = os.environ["API_KEY"]
    secret_key = os.environ["SECRET_KEY"]

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
    secret_key = os.environ["SECRET_KEY"]
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
    api_key = os.environ["API_KEY"]

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
    assert response.text == '"ERROR"'


def test_generate_jwt():
    response = client.get("/generate-jwt")
    assert response.status_code == 200
    assert "jwt" in response.json()
