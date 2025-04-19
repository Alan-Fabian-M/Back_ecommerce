import cloudinary
import cloudinary.uploader

# Asegúrate de que se cargue la configuración al importar
from .cloudinary_config import *

def subir_imagen(archivo, carpeta="productos"):
    try:
        resultado = cloudinary.uploader.upload(archivo, folder=carpeta)
        return resultado.get("secure_url")
    except Exception as e:
        print("❌ Error al subir imagen a Cloudinary:", e)
        return None