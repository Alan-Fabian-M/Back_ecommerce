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
        data = cupon_schema.load(request.json)  # Cargar y validar los datos con Marshmallow

        # Obtener la fecha actual (sin la hora) para fecha_inicio
        fecha_inicio = datetime.now().date()

        # Asignar la fecha de inicio como la fecha actual
        data.fecha_inicio = fecha_inicio

        # Calcular fecha_fin como 30 días después de fecha_inicio
        fecha_fin = fecha_inicio + timedelta(days=30)
        data.fecha_fin = fecha_fin

        db.session.add(data)
        db.session.commit()
        return jsonify(cupon_schema.dump(data)), 201  # Devolver el cupón creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Actualizar un cupón existente
@cupon_bp.route('/cupones/<int:id>', methods=['PUT'])
def update_cupon(id):
    try:
        cupon = Cupon.query.get_or_404(id)  # Buscar el cupón por ID
        data = cupon_schema.load(request.json)  # Cargar los nuevos datos
        for key, value in data.items():
            setattr(cupon, key, value)  # Actualizar el cupón
        db.session.commit()
        return jsonify(cupon_schema.dump(cupon))  # Devolver el cupón actualizado
    except Exception as e:
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
