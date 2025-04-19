# app/utils/utils.py
from app import db
from ..models.producto_model import Producto
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

    
def cliente_id(data):
    try:
        cliente_id = get_jwt_identity() # Asumiendo que el ID del cliente está en el token
        data['cliente_id'] = cliente_id
        
        return data  # Devolver el movimiento actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    