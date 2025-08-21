from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os
from app.utils.jwt_handler import verify_jwt
from app.utils.jwt_handler import create_jwt
from dotenv import load_dotenv

load_dotenv() # Esto solo sirve localmente. En Azure, no carga .env, sino variables del entorno del sistema

app = FastAPI()

EXPECTED_API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


class DevOpsPayload(BaseModel):
    message: str
    to: str
    from_: str = Field(..., alias="from")
    timeToLifeSec: int


@app.post("/DevOps")
async def devops_endpoint(
    payload: DevOpsPayload,
    X_Parse_REST_API_Key: Optional[str] = Header(None),
    X_JWT_KWY: Optional[str] = Header(None)
):
    if not X_Parse_REST_API_Key or X_Parse_REST_API_Key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    if not X_JWT_KWY or not verify_jwt(X_JWT_KWY):
        raise HTTPException(status_code=403, detail="Invalid or missing JWT")

    return {"message": f"Hello {payload.to} your message will be send"}

@app.api_route("/DevOps", methods=["GET", "PUT", "DELETE", "PATCH"])
async def invalid_methods():
    return "ERROR"


@app.get("/generate-jwt")
def generate_jwt_endpoint():
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY is not set")

    token = create_jwt({"user": "test"}, secret_key=SECRET_KEY, expires_in=604800)
    return {"jwt": token}
