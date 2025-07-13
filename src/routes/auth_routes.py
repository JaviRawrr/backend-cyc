from litestar import Router, post, Request, Response 
from litestar.exceptions import NotAuthorizedException
from src.database import get_db_connection
from src.auth.services import create_access_token
from src.schemas.auth_schemas import LoginRequest, LoginResponse, LogoutResponse
from passlib.context import CryptContext

# Instancia para manejar el hashing de contraseñas
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Función para verificar contraseñas ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña plana contra una contraseña hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

# --- Define los manejadores de ruta primero con los decoradores de Litestar ---
@post("/login") # <--- ¡Aquí usamos el decorador 'post' directamente de Litestar!
async def login(data: LoginRequest) -> LoginResponse:
    """
    Autentica a un usuario y retorna un token JWT.
    """
    username = data.username
    plain_password = data.password

    conn = None
    try:
        conn = await get_db_connection()
        user_row = await conn.fetchrow("SELECT id, username, password, role FROM users WHERE username = $1", username)

        if not user_row:
            raise NotAuthorizedException("Credenciales inválidas")

        if not verify_password(plain_password, user_row['password']):
            raise NotAuthorizedException("Credenciales inválidas")

        payload = {
            "user_id": user_row['id'],
            "username": user_row['username'],
            "role": user_row['role']
        }
        token = create_access_token(payload)

        return LoginResponse(
            message="Login successful",
            access_token=token,
            token_type="bearer",
            role=user_row['role']
        )
    except NotAuthorizedException as e:
        # Re-lanza la excepción NotAuthorizedException para que Litestar la maneje
        raise e
    except Exception as e:
        print(f"Error inesperado durante el login: {e}")
        # Lanza una excepción genérica para el cliente
        raise NotAuthorizedException("Ocurrió un error interno durante el inicio de sesión.")
    finally:
        if conn:
            await conn.close()

@post("/logout") # <--- ¡También usamos el decorador 'post' directamente de Litestar!
async def logout() -> LogoutResponse:
    """
    Simula el cierre de sesión del usuario.
    """
    return LogoutResponse(message="Sesión cerrada correctamente")

# --- Luego, inicializa el Router CON sus manejadores de ruta ---
# Esto hace que las funciones 'login' y 'logout' sean parte de 'auth_router',
# y la ruta base '/auth' se aplicará a ellas.
auth_router = Router(path="/auth", route_handlers=[login, logout])