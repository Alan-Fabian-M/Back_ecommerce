# app/utils/utils.py
from app import db
from ..models.marca_model import Marca
from flask import jsonify

    
def marca_id(data):
    try:
        if data.get("marca_nombre"):
            
            marca_nombre = data.get("marca_nombre")
            if not marca_nombre:
                raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

            marca = Marca.query.filter_by(nombre=marca_nombre).first()
            if not marca:
                raise ValueError(f"No existe una marca con el nombre '{marca}'.")

            data["marca_id"] = marca.id
            data.pop("marca_nombre")
            return data
        else:
            return data
    except Exception as e:
        raise e