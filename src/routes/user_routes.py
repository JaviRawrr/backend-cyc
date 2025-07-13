from litestar import Router, get, Request
from litestar.exceptions import NotAuthorizedException
from src.database import get_db_connection
from src.auth.services import decode_access_token
from src.schemas.user_schemas import UserResponse, UserData
from typing import List

# Define la función de ruta primero

@get("/")
async def get_users(request: Request) -> List[UserResponse]:
    """
    Retorna la lista de usuarios, filtrada por el rol del usuario autenticado.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise NotAuthorizedException("Token no proporcionado o formato inválido. Se espera 'Bearer [token]'")

    token = auth_header.split("Bearer ")[1]

    try:
        token_payload = decode_access_token(token)
        current_user_role = token_payload['role']
        current_username = token_payload['username']
    except ValueError as e:
        raise NotAuthorizedException(str(e))
    except Exception:
        raise NotAuthorizedException("Token inválido o corrupto")

    conn = None
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("SELECT username, role, name, email FROM users")

        all_users: List[UserResponse] = [
            UserResponse(
                username=row['username'],
                role=row['role'],
                data=UserData(name=row['name'], email=row['email'])
            )
            for row in rows
        ]

        if current_user_role == "admin":
            return all_users
        elif current_user_role == "supervisor":
            filtered_users = [user for user in all_users if user['role'] in ["supervisor", "usuario"]]
            return filtered_users
        elif current_user_role == "usuario":
            filtered_users = [user for user in all_users if user['username'] == current_username]
            return filtered_users
        else:
            raise NotAuthorizedException("Rol desconocido")
    except Exception as e:
        print(f"Error en get_users: {e}")
        raise NotAuthorizedException("Ocurrió un error al obtener los datos de usuarios.")
    finally:
        if conn:
            await conn.close()

# Inicializa el Router y la función de 'route_handlers'
user_router = Router(path="/users", route_handlers=[get_users])