import os
import subprocess
from app import create_app
from flask_migrate import upgrade, migrate, init

app = create_app()

def ejecutar_migraciones():
    # Verifica si la carpeta 'migrations' existe, si no, la inicializa.
    if not os.path.exists("migrations"):
        os.system("flask db init")  # Inicializa las migraciones

    # Ejecuta las migraciones
    os.system("flask db migrate")  # Genera las migraciones
    os.system("flask db upgrade")  # Aplica las migraciones a la base de datos



if __name__ == '__main__':
    # Primero, aseguramos que las migraciones estén hechas
    with app.app_context():
        ejecutar_migraciones()  # Ejecuta migraciones

        # Luego, poblar la base de datos con datos falsos
        # ejecutar_seeders()

    # Ahora se inicia la aplicación
    app.run(debug=True)
