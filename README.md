🚀 Instalación
Clona el repositorio:

    git clone https://github.com/tuusuario/ecommerce-backend.git

    cd ecommerce-backend


Crea y activa un entorno virtual:

    python -m venv venv

    # Windows
        venv\Scripts\activate
    # Linux/Mac
        source venv/bin/activate


Instala las dependencias:

    pip install -r requirements.txt


⚙️ Configuración
Crea un archivo .env o edita el archivo de configuración con tus datos:

    DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/ecommerce_db
    SECRET_KEY=tu_clave_secreta


🗃️ Migraciones y Seeders
Inicializa la base de datos (si es la primera vez):

    alembic upgrade head


Carga los datos iniciales con seeders (faker):

    python -m app.seeders.faker_seeder

🔐 Autenticación con JWT
Los usuarios reciben un token JWT al autenticarse. Ese token incluye:

{
  "Token": "eyJhbGciOi...",
  "Rol": "admin"
}

Puedes usar este token en tus peticiones protegidas agregando un header:

    Authorization: Bearer <tu-token>

🧪 Ejecutar el servidor
    
    python run.py

El servidor se iniciará en: http://127.0.0.1:5000


📁 Estructura del proyecto

    ecommerce-2/
    │
    ├── app/
    │   ├── models/           # Modelos de SQLAlchemy
    │   ├── routes/           # Endpoints de la API
    │   ├── seeders/          # Archivos para poblar datos iniciales
    │   ├── __init__.py       # Inicialización del app
    │   ├── config.py         # Configuraciones
    │   └── main.py           # Lógica para correr la app
    │
    ├── alembic/              # Migrations de base de datos
    ├── requirements.txt      # Dependencias
    ├── run.py                # Punto de entrada