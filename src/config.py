import os
# --- Configuración de la Base de Datos PostgreSQL ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_admin:phe2Q1yNDx8i89mC9EGQ3nulMcJvb5QB@dpg-d1p8mrvfte5s73c3ffrg-a.ohio-postgres.render.com/cyc_4rar")

# --- Otras Configuraciones (Opcional) ---
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_super_segura_aqui_para_desarrollo")
