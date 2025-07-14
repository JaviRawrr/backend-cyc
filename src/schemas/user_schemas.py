from typing import Literal, Optional
from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3)]
    password: Annotated[str, StringConstraints(min_length=6)] 
    name: str
    email: EmailStr
    role: str  # admin, supervisor, usuario

class UserUpdate(BaseModel):
    password: Optional[Annotated[str, StringConstraints(min_length=6)]] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "supervisor", "usuario"]] = None
    
class UserData(BaseModel):
    """Esquema para los datos adicionales del usuario."""
    name: str
    email: str

class UserResponse(BaseModel):
    """Esquema para un solo usuario en la lista de respuesta."""
    username: str
    role: Literal["admin", "supervisor", "usuario"]
    data: UserData # Anidamos el modelo UserData aquí