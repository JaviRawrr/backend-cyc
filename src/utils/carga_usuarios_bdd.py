# src/utils/carga_usuarios_bdd.py

import asyncio
import json
import os
import unicodedata

# Carga las variables de entorno para que este script funcione de forma independiente
from dotenv import load_dotenv
load_dotenv()


# Importa las funciones necesarias desde tu proyecto
from src.database import get_db_connection
from src.auth.services import get_password_hash


async def cargar_usuarios_desde_json():
    """
    Carga y procesa usuarios desde 'usuarios.json' e los inserta/actualiza en la base de datos.
    Las contraseñas se hashean usando el username como valor inicial.
    """
    conn = None
    try:
        conn = await get_db_connection()
        print("Conexión a la base de datos establecida para carga de usuarios.")

        # Manejo del usuario 'admin' por defecto
        admin_username = 'admin'
        admin_password_plain = 'admin' # Contraseña en texto plano para el admin inicial de la app
        admin_password_hashed = get_password_hash(admin_password_plain) # Hasheamos esta contraseña

        await conn.execute("""
            INSERT INTO users (username, password, role, name, email)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (username) DO UPDATE SET
                password = EXCLUDED.password,
                role = EXCLUDED.role,
                name = EXCLUDED.name,
                email = EXCLUDED.email;
        """, admin_username, admin_password_hashed, 'admin', 'Administrador', 'admin@example.com')
        print(f"Usuario '{admin_username}' verificado/añadido (contraseña para la aplicación hasheada).")


        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'usuarios.json')

        if not os.path.exists(json_file_path):
            print(f"ADVERTENCIA: El archivo {json_file_path} no se encontró. No se cargarán datos de usuarios desde JSON.")
            return

        with open(json_file_path, 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        print(f"Cargando {len(users_data)} usuarios desde usuarios.json (y hasheando sus contraseñas iniciales)...")

        async with conn.transaction():
            for user in users_data:
                normalized_name = unicodedata.normalize('NFKD', user['nombre']).encode('ascii', 'ignore').decode('utf-8')
                username = normalized_name.replace(" ", "_").lower()

                plain_password = username # La contraseña inicial es el username generado
                hashed_password = get_password_hash(plain_password) # Hasheamos esta contraseña

                role = user['rol']
                name = user['nombre']
                email = f"{username}@example.com"
                renta_mensual = user['renta_mensual']

                await conn.execute(
                    """
                    INSERT INTO users (username, password, role, name, email, renta_mensual)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (username) DO UPDATE SET
                        password = EXCLUDED.password,
                        role = EXCLUDED.role,
                        name = EXCLUDED.name,
                        email = EXCLUDED.email,
                        renta_mensual = EXCLUDED.renta_mensual;
                    """, username, hashed_password, role, name, email, renta_mensual
                )
        print("Datos de usuarios cargados/actualizados exitosamente desde usuarios.json (contraseñas hasheadas).")

    except Exception as e:
        print(f"Error durante la carga de datos de usuarios: {e}")
        # No re-lanzamos si es un script independiente, pero sí mostramos el error
    finally:
        if conn:
            await conn.close()
            print("Conexión a la base de datos cerrada después de la carga de usuarios.")

if __name__ == "__main__":
    # Si ejecutas este archivo directamente, llama a la función principal
    asyncio.run(cargar_usuarios_desde_json())