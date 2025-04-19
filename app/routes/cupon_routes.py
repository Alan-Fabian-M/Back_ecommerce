from flask import Blueprint, request, jsonify
from ..models.cupon_model import Cupon
from ..schemas.cupon_schema import CuponSchema
from app import db
from datetime import datetime, timedelta

cupon_bp = Blueprint('cupon_bp', __name__)
cupon_schema = CuponSchema(session=db.session)
cupones_schema = CuponSchema(many=True)

# Obtener todos los cupones
@cupon_bp.route('/cupones', methods=['GET'])
def get_cupones():
    try:
        cupones = Cupon.query.all()
        return jsonify(cupones_schema.dump(cupones))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un cupón por ID
@cupon_bp.route('/cupones/<int:id>', methods=['GET'])
def get_cupon(id):
    try:
        cupon = Cupon.query.get_or_404(id)
        return jsonify(cupon_schema.dump(cupon))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo cupón
@cupon_bp.route('/cupones', methods=['POST'])
def add_cupon():
    try:
        # Obtener los datos enviados por el cliente
        data = request.json
        
        # Validar y cargar el objeto Cupon
        cupon = cupon_schema.load(data)

        # Guardar en la base de datos
        db.session.add(cupon)
        db.session.commit()

        return jsonify(cupon_schema.dump(cupon)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cupon_bp.route('/cupones/<int:id>', methods=['PUT'])
def update_cupon(id):
    try:
        cupon = Cupon.query.get_or_404(id)

        data = cupon_schema.load(request.get_json(), partial=True)
        for key in request.json:
            setattr(cupon, key, getattr(data, key))

        db.session.commit()
        return jsonify(cupon_schema.dump(cupon)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un cupón
@cupon_bp.route('/cupones/<int:id>', methods=['DELETE'])
def delete_cupon(id):
    try:
        cupon = Cupon.query.get_or_404(id)  # Buscar el cupón por ID
        db.session.delete(cupon)  # Eliminar el cupón
        db.session.commit()
        return jsonify({'message': 'Cupón eliminado', 'data': cupon_schema.dump(cupon)}), 200  # Devolver el cupón eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
