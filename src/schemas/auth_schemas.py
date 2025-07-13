from pydantic import BaseModel
from typing import Literal

class LoginRequest(BaseModel):
    """Esquema para la solicitud de inicio de sesión."""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Esquema para la respuesta exitosa del login."""
    message: str
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    role: Literal["admin", "supervisor", "usuario"]

class LogoutResponse(BaseModel):
    """Esquema para la respuesta de cierre de sesión."""
    message: str