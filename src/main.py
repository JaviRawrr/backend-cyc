from litestar import Litestar, Router
from src.database import init_db    
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import SecurityScheme
# Importa Routers 
from src.routes.auth_routes import auth_router
from src.routes.user_routes import user_router

# --- Configuración CORS ---
cors_config = CORSConfig(
    allow_origins=["https://frontend-cyc.onrender.com","http://localhost:8000"], #Para entorno de Prueba
    allow_headers=["Authorization", "Content-Type"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_credentials=True,
)
# --- Configuración de OpenAPI (Swagger UI) ---
openapi_config = OpenAPIConfig(
    title="API de Gestión de Usuarios (CyC)",
    version="1.0.0",
    description="API con autenticación JWT.",
    security=[{"bearerAuth": []}],
)

openapi_config.components.security_schemes = {
    "bearerAuth": SecurityScheme(
        type="http",
        scheme="bearer",
        bearer_format="JWT",
        description="Autenticación con token JWT. Usa: Bearer <token>"
    )
}

# --- Creación de la Aplicación Litestar ---
app = Litestar(
    #Declración de las rutas a utilizar
    route_handlers=[
    Router(
        path="/api-cyc",
        route_handlers=[
            auth_router,
            user_router
        ]
    )
],
    on_startup=[init_db],
    cors_config=cors_config,
    openapi_config=openapi_config, # Habilita OpenAPI/SwaggerAPI
)
