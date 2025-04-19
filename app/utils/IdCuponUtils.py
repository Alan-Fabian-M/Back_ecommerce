# app/utils/utils.py
from app import db
from ..models.cupon_model import Cupon
from flask import jsonify

    
def cupon_id(data):
    try:
        cupon_nombre = data.get("cupon_nombre")
        if not cupon_nombre:
            raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

        cupon = Cupon.query.filter_by(nombre=cupon_nombre).first()
        if not cupon:
            raise ValueError(f"No existe un producto con el nombre '{cupon}'.")

        data["cupon_id"] = cupon.id
        data.pop("cupon_nombre")
        return data
    except Exception as e:
        raise e