# src/schemas/user_schemas.py
from pydantic import BaseModel
from typing import Literal

class UserData(BaseModel):
    """Esquema para los datos adicionales del usuario."""
    name: str
    email: str

class UserResponse(BaseModel):
    """Esquema para un solo usuario en la lista de respuesta."""
    username: str
    role: Literal["admin", "supervisor", "usuario"]
    data: UserData # Anidamos el modelo UserData aquí