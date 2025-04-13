import os
from datetime import timedelta

class Config:
    
    #nombre de usuario , contraseña, nombre de la base de datos
    #'postgresql://Nombre de usuario:contraseña@localhost/nombre de la base de datos'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:alan123@localhost/ecommerce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'
    JWT_SECRET_KEY = '123456789'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)