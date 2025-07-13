import os

# --- Configuración de la Base de Datos PostgreSQL ---
# Render inyectará la URL de la base de datos como una variable de entorno.
# Usamos os.getenv() para leerla. Si no existe (ej. en desarrollo local),
# puedes poner una URL de desarrollo local aquí.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_admin:phe2Q1yNDx8i89mC9EGQ3nulMcJvb5QB@dpg-d1p8mrvfte5s73c3ffrg-a.ohio-postgres.render.com/cyc_4rar")

# --- Otras Configuraciones (Opcional) ---
# Clave secreta para manejo de sesiones o JWT (¡Genera una fuerte para producción!)
# En producción, esto también debería ser una variable de entorno.
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_super_segura_aqui_para_desarrollo")
