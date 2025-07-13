import asyncpg
import os
import json
import unicodedata
from src.auth.services import get_password_hash
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app_admin:phe2Q1yNDx8i89mC9EGQ3nulMcJvb5QB@dpg-d1p8mrvfte5s73c3ffrg-a.ohio-postgres.render.com/cyc_4rar")

async def get_db_connection():
    """
    Establece y retorna una conexión asíncrona a la base de datos PostgreSQL.
    Usa la DATABASE_URL configurada en el .env.
    """
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        # Re-lanzar la excepción para que el llamador pueda manejar el fallo de conexión
        raise

async def init_db():
    """
    Inicializa la base de datos: crea la tabla 'users' si no existe.
    La carga de usuarios se realiza en un script separado (utils/carga_usuarios_bdd.py).
    """
    conn = None
    try:
        conn = await get_db_connection()
        print("Conexión a la base de datos establecida para inicialización de la estructura.")

        # Crear la tabla de usuarios si no existe
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'usuario',
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                renta_mensual NUMERIC(10, 2)
            );
        """)
        print("Tabla 'users' verificada/creada.")

    except Exception as e:
        print(f"Error durante la inicialización de la estructura de la base de datos: {e}")
        raise
    finally:
        if conn:
            await conn.close()
            print("Conexión a la base de datos cerrada después de la inicialización de la estructura.")