import os
from datetime import timedelta

class Config:
    # Usa la variable de entorno DATABASE_URL que Render genera automáticamente
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = "postgresql://si2_user:G8OQJC0Yt9WREGNUVylTxdnNv63RpO47@dpg-cvu0lr7gi27c73acfn20-a.oregon-postgres.render.com/si2"
    
    CLOUDINARY_CLOUD_NAME = "dozywphod"
    CLOUDINARY_API_KEY = "441626374645742"
    CLOUDINARY_API_SECRET = "qJAFgRUbyHSVc_SitfIXj0ELXFI"
    
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:alan123@localhost:5432/pruebas"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Claves seguras desde variables de entorno
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-jwt')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
