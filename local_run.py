import os
from app import create_app

app = create_app()

def ejecutar_migraciones():
    if not os.path.exists("migrations"):
        os.system("flask db init")
    os.system("flask db migrate")
    os.system("flask db upgrade")

if __name__ == "__main__":
    with app.app_context():
        ejecutar_migraciones()
    app.run(debug=True)
