# app/utils/utils.py
from app import db
from ..models.metodo_pago_model import MetodoPago
from flask import jsonify

    
def metodo_pago_id(data):
    try:
        if data.get("metodo_pago_nombre"):
            metodo_pago = data.get("metodo_pago_nombre")
            if not metodo_pago:
                raise ValueError("El campo 'producto_nombre' es requerido en el diccionario.")

            metodo_pago = MetodoPago.query.filter_by(nombre=metodo_pago).first()
            if not metodo_pago:
                raise ValueError(f"No existe un producto con el nombre '{metodo_pago}'.")

            data["metodo_pago_id"] = metodo_pago.id
            data.pop("metodo_pago_nombre")
            return data
        else:
            return data
    except Exception as e:
        raise e