from flask import Blueprint, request, jsonify
from ..models.movimiento_model import Movimiento
from ..schemas.movimiento_schema import MovimientoSchema
from app import db  # Asegúrate de importar db desde tu archivo de configuración
from flask_jwt_extended import jwt_required

movimiento_bp = Blueprint('movimiento_bp', __name__)
movimiento_schema = MovimientoSchema(session=db.session)
movimientos_schema = MovimientoSchema(many=True)

# Obtener todos los movimientos
@movimiento_bp.route('/movimientos', methods=['GET'])
@jwt_required()
def get_movimientos():
    try:
        movimientos = Movimiento.query.all()
        return jsonify(movimientos_schema.dump(movimientos))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un movimiento por ID
@movimiento_bp.route('/movimientos/<int:id>', methods=['GET'])
@jwt_required()
def get_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)
        return jsonify(movimiento_schema.dump(movimiento))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo movimiento
@movimiento_bp.route('/movimientos', methods=['POST'])
@jwt_required()
def add_movimiento():
    try:
        data = movimiento_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        # nuevo_movimiento = Movimiento(**data)  # Crear una nueva instancia de Movimiento
        db.session.add(data)
        db.session.commit()
        return jsonify(movimiento_schema.dump(data)), 201  # Devolver el nuevo movimiento creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un movimiento existente
@movimiento_bp.route('/movimientos/<int:id>', methods=['PUT'])
@jwt_required()
def update_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)  # Buscar el movimiento por ID
        data = movimiento_schema.load(request.json)  # Cargar los nuevos datos
        for key, value in data.items():
            setattr(movimiento, key, value)  # Actualizar los campos del movimiento
        db.session.commit()
        return jsonify(movimiento_schema.dump(movimiento))  # Devolver el movimiento actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un movimiento
@movimiento_bp.route('/movimientos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)  # Buscar el movimiento por ID
        db.session.delete(movimiento)  # Eliminar el movimiento
        db.session.commit()
        return jsonify({'message': 'Movimiento eliminado', 'data': movimiento_schema.dump(movimiento)}), 200  # Devolver el movimiento eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
