import jwt
from litestar import Request
from litestar.exceptions import NotAuthorizedException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()

# Hashing para contraseñas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") 

#Obtiene clave secreta desde el env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user_payload_from_request(request: Request) -> dict:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise NotAuthorizedException("Token no proporcionado o formato inválido.")
    
    token = auth_header.removeprefix("Bearer ").strip()
    try:
        return decode_access_token(token)
    except ValueError as e:
        raise NotAuthorizedException(str(e))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica la contraseña con la contraseña hasheada
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashea una contraseña
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")