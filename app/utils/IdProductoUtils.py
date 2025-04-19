# app/utils/utils.py
from app import db
from ..models.producto_model import Producto
from flask import jsonify

    
def producto_id(data):
    try:
        if data.get("producto_nombre"):
            producto_nombre = data.get("producto_nombre")
            if not producto_nombre:
                raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

            producto = Producto.query.filter_by(nombre=producto_nombre).first()
            if not producto:
                raise ValueError(f"No existe un producto con el nombre '{producto_nombre}'.")

            data["producto_id"] = producto.id
            data.pop("producto_nombre")
            return data
        else:
            return data
    except Exception as e:
        raise e
    