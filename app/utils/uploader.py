from .cloudinary_config import cloudinary

def subir_imagen(archivo, carpeta="productos"):
    respuesta = cloudinary.uploader.upload(archivo, folder=carpeta)
    return respuesta.get("secure_url")