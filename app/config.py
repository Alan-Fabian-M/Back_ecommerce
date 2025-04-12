import os

class Config:
    
    #nombre de usuario , contraseña, nombre de la base de datos
    #'postgresql://Nombre de usuario:contraseña@localhost/nombre de la base de datos'
    SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:password@localhost:puerto/nombre_basedatos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta")