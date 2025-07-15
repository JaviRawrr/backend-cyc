# 🐍 Backend: Sistema de Gestión CyC API

Este repositorio contiene el código fuente del backend (API) para el Sistema de Gestión de Usuarios CyC, construido con Litestar y Python. Proporciona los endpoints necesarios para la gestión de usuarios, incluyendo autenticación, creación, lectura, actualización y eliminación (CRUD).

---

## 🚀 Cómo Ponerlo en Marcha (Desarrollo Web)

    Abre tu Navegador Web Preferido: Chrome, Firefox, Edge, Safari, etc.

    Introduce la URL del Frontend: https://frontend-cyc.onrender.com/

    Una vez cargada, la aplicación te redirigirá automáticamente a la página de inicio de sesión si aún no has iniciado sesión.

    💻 Conexión al Backend (API)
    El frontend que estás utilizando se conecta a una API de backend para gestionar los usuarios. Esta API también está desplegada y accesible públicamente.

    URL Base de la API:

    La API de backend a la que se conecta tu frontend se encuentra en:
    https://backend-cyc.onrender.com/

    Puedes verificar si la API está activa y funcionando correctamente visitando la documentación en Swagger:
    https://backend-cyc.onrender.com/schema/swagger

    🎉 ¡Listo para Usar!
    ¡Y eso es todo! Te sugiero ingresar con las siguientes credenciales para probar las funcionalidades de administrador:

    Usuario: admin
    Contraseña: admin


## 🚀 Cómo Ponerlo en Marcha (Desarrollo Local)

Sigue estos pasos para configurar y ejecutar el backend de la aplicación en tu máquina local.

### 📋 Prerrequisitos

Asegúrate de tener instalado lo siguiente:

* **Python 3.^** 
* **pip** 
* **git**

### 💻 Pasos de Instalación y Ejecución

1.  **Clonar el Repositorio:**
    Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio:

    git clone https://github.com/JaviRawrr/backend-cyc.git
    cd backend-cyc


2.  **Crear y Activar un Entorno Virtual:**
    Es una buena práctica crear un entorno virtual para aislar las dependencias del proyecto.

    python -m venv venv

    * **En Windows:**
        .\venv\Scripts\activate

    * **En macOS/Linux:**
        source venv/bin/activate


3.  **Instalar Dependencias:**
    Con el entorno virtual activado, instala todas las dependencias listadas en `requirements.txt`:

    pip install -r requirements.txt


4.  **Configuración de Variables de Entorno:**
    # BDD - Credenciales de conexión a la base de datos
    DATABASE_URL="postgresql://app_admin:phe2Q1yNDx8i89mC9EGQ3nulMcJvb5QB@dpg-d1p8mrvfte5s73c3ffrg-a.ohio-postgres.render.com/cyc_4rar"
    # JWT - Clave secreta para la generación y verificación de tokens de seguridad
    SECRET_KEY="cdfb9c92c72cc940477293908b5803fa3cc6384a89d93ddb07978658579b8055"

5.  **Base de Datos:**
    Para este proyecto, la base de datos ya se encuentra desplegada y configurada en Render. 
    Esto significa que no necesitas ejecutar migraciones localmente ni preocuparte 
    por la configuración inicial de la base de datos en tu entorno de desarrollo web ni local.

6.  **Iniciar el Servidor de la API:**
    Puedes iniciar el servidor Litestar usando `uvicorn`:

    uvicorn src:main --reload --host 0.0.0.0 --port 8000

    El backend estará accesible en `http://localhost:8000` (o el puerto que hayas configurado).
    Puedes verificar el estado de la API visitando `http://localhost:8000/schema/swagger/` para ver la documentación de OpenAPI (Swagger/ReDoc).

---

## 🛠️ Estructura del Proyecto

* `app.py`: Archivo principal de la aplicación Litestar.
* `models/`: Definiciones de modelos de datos.
* `routes/`: Módulos con los diferentes routers de la API.
* `services/`: Lógica de negocio y operaciones de base de datos.
* `schemas/`: Esquemas Pydantic para validación de datos.
* `utils/`: Script de población de la BDD.
* `requirements.txt`: Listado de todas las dependencias de Python.
