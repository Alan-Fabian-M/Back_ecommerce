# app/utils/utils.py
from app import db
from ..models.rol_model import Rol
from flask import jsonify

    
def rol_id(data):
    try:
        rol_nombre = data.get("rol_nombre")
        if not rol_nombre:
            raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

        rol = Rol.query.filter_by(nombre=rol_nombre).first()
        if not rol:
            raise ValueError(f"No existe un producto con el nombre '{rol}'.")

        data["rol_id"] = rol.id
        data.pop("rol_nombre")
        return data
    except Exception as e:
        raise e