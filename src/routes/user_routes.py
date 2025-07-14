from litestar import Router, get, Request, post, put
from litestar.exceptions import NotAuthorizedException
from src.database import get_db_connection
from src.auth.services import decode_access_token, get_password_hash, get_user_payload_from_request
from src.schemas.user_schemas import UserCreate, UserResponse, UserData, UserUpdate
from typing import List

@get("/mostrar-usuarios", tags=["Usuarios"])
async def get_users(request: Request) -> List[UserResponse]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise NotAuthorizedException("Token no proporcionado o formato inválido. Se espera 'Bearer [token]'")

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        token_payload = decode_access_token(token)
        current_user_role = token_payload['role']
        current_username = token_payload['username']
    except Exception as e:
        raise NotAuthorizedException(f"Token inválido: {str(e)}")

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

        match current_user_role:
            case "admin":
                return all_users
            case "supervisor":
                return [u for u in all_users if u.role in {"supervisor", "usuario"}]
            case "usuario":
                return [u for u in all_users if u.username == current_username]
            case _:
                raise NotAuthorizedException("Rol desconocido")
    finally:
        if conn:
            await conn.close()

@post("/crear-usuario", tags=["Usuarios"])
async def create_user(request: Request, data: UserCreate) -> UserResponse:
    payload = get_user_payload_from_request(request)
    rol_actual = payload["role"]

    if rol_actual not in ("admin", "supervisor"):
        raise NotAuthorizedException("No tienes permisos para crear usuarios")

    if rol_actual == "supervisor" and data.role == "admin":
        raise NotAuthorizedException("Un supervisor no puede crear usuarios admin")

    conn = await get_db_connection()
    try:
        hashed_pwd = get_password_hash(data.password)

        await conn.execute(
            """
            INSERT INTO users (username, password, name, email, role)
            VALUES ($1, $2, $3, $4, $5)
            """,
            data.username, hashed_pwd, data.name, data.email, data.role
        )

        return UserResponse(
            username=data.username,
            role=data.role,
            data=UserData(name=data.name, email=data.email)
        )
    finally:
        await conn.close()

@put("/actualizar-usuario/{username:str}", tags=["Usuarios"])
async def update_user(request: Request, username: str, data: UserUpdate) -> UserResponse:
    payload = get_user_payload_from_request(request)
    current_role = payload["role"]
    current_username = payload["username"]

    # Seguridad por rol
    if current_role == "usuario" and username != current_username:
        raise NotAuthorizedException("No puedes editar a otros usuarios.")
    if current_role == "supervisor":
        # No puede modificar admins
        conn = await get_db_connection()
        try:
            target_user = await conn.fetchrow("SELECT role FROM users WHERE username = $1", username)
            if not target_user:
                raise NotAuthorizedException("Usuario no encontrado.")
            if target_user["role"] == "admin":
                raise NotAuthorizedException("No puedes modificar un usuario admin.")
        finally:
            await conn.close()

    fields = []
    values = []

    if data.password:
        fields.append("password = $1")
        values.append(get_password_hash(data.password))
    if data.name:
        fields.append(f"name = ${len(values)+1}")
        values.append(data.name)
    if data.email:
        fields.append(f"email = ${len(values)+1}")
        values.append(data.email)
    if data.role and current_role == "admin":  # solo admin puede cambiar roles
        fields.append(f"role = ${len(values)+1}")
        values.append(data.role)

    if not fields:
        raise NotAuthorizedException("No hay datos válidos para actualizar.")

    update_query = f"UPDATE users SET {', '.join(fields)} WHERE username = ${len(values)+1}"

    values.append(username)

    conn = await get_db_connection()
    try:
        await conn.execute(update_query, *values)

        row = await conn.fetchrow("SELECT username, role, name, email FROM users WHERE username = $1", username)

        return UserResponse(
            username=row["username"],
            role=row["role"],
            data=UserData(name=row["name"], email=row["email"])
        )
    finally:
        await conn.close()

from litestar import delete
from litestar.response import Response

@delete("/eliminar-usuario/{username:str}", tags=["Usuarios"], status_code=200)
async def delete_user(request: Request, username: str) -> Response:
    payload = get_user_payload_from_request(request)
    current_role = payload["role"]
    current_username = payload["username"]

    if current_role == "usuario":
        raise NotAuthorizedException("No tienes permisos para eliminar usuarios.")

    conn = await get_db_connection()
    try:
        # Validar existencia del usuario
        target = await conn.fetchrow("SELECT role FROM users WHERE username = $1", username)
        if not target:
            raise NotAuthorizedException("Usuario no encontrado.")

        target_role = target["role"]

        if current_role == "supervisor" and target_role == "admin":
            raise NotAuthorizedException("No puedes eliminar usuarios con rol admin.")

        # Ejecutar eliminación
        await conn.execute("DELETE FROM users WHERE username = $1", username)

        return Response(
            content=f"Usuario '{username}' eliminado correctamente.",
            media_type="text/plain",
            status_code=200
        )
    finally:
        await conn.close()

        
# Inicializa el Router y la función de 'route_handlers'
user_router = Router(path="/users", route_handlers=[get_users, create_user,update_user,delete_user])