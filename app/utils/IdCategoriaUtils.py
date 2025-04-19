# app/utils/utils.py
from app import db
from ..models.categoria_model import Categoria
from flask import jsonify

    
def categoria_id(data):
    try:
        if data.get("categoria_nombre"):
            
            categoria_nombre = data.get("categoria_nombre")
            if not categoria_nombre:
                raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

            categoria = Categoria.query.filter_by(nombre=categoria_nombre).first()
            if not categoria:
                raise ValueError(f"No existe una categoria con el nombre '{categoria}'.")

            data["categoria_id"] = categoria.id
            data.pop("categoria_nombre")
            return data
        else:
            return data
    except Exception as e:
        raise e