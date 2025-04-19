from ..utils.IdProductoUtils import producto_id
from flask import Blueprint, request, jsonify
from ..models.movimiento_model import Movimiento
from ..schemas.movimiento_schema import MovimientoSchema
from app import db  # Asegúrate de importar db desde tu archivo de configuración
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_cors import cross_origin
from ..utils.RegisterBitacoraUtils import registrar_en_bitacora
from datetime import datetime

movimiento_bp = Blueprint('movimiento_bp', __name__)
movimiento_schema = MovimientoSchema(session=db.session)
movimientos_schema = MovimientoSchema(many=True)

# Obtener todos los movimientos
@movimiento_bp.route('/movimientos', methods=['GET'])
@jwt_required()
@cross_origin()
def get_movimientos():
    try:
        movimientos = Movimiento.query.all()
        return jsonify(movimientos_schema.dump(movimientos))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un movimiento por ID
@movimiento_bp.route('/movimientos/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)
        return jsonify(movimiento_schema.dump(movimiento))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
@movimiento_bp.route('/movimientos', methods=['POST'])
@jwt_required()
@cross_origin()
def add_movimiento():
    try:
        data = request.get_json()
        # Obtener el ID del usuario del token JWT
        usuario_id = get_jwt_identity()
        # Agregar el usuario_codigo a los datos antes de cargar al esquema
        data['usuario_codigo'] = usuario_id
        # Cargar los datos del cuerpo de la solicitud, incluyendo el usuario_codigo
        data["fecha"] = datetime.now().date().isoformat()
        data = producto_id(data)
        nuevo_movimiento = movimiento_schema.load(data)
        # Crear una nueva instancia de Movimiento con los datos cargados
        
        
        
        db.session.add(nuevo_movimiento)
        db.session.commit()
        # Serializar el nuevo movimiento para la respuesta
        movimiento = movimiento_schema.dump(nuevo_movimiento)
        # Registrar la acción en la bitácora
        registrar_en_bitacora(usuario_id, movimiento["tipomovimiento"], "realizando movimiento")
        return jsonify(movimiento), 201  # Devolver el nuevo movimiento creado
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Actualizar un movimiento existente
@movimiento_bp.route('/movimientos/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)

        data = request.get_json()
        data = producto_id(data)
        
        # data = movimiento_schema.load(request.get_json(), partial=True)
        
        
        for key, value in data.items():
            if hasattr(movimiento, key):
                setattr(movimiento, key, value)

        
        # usuario_id = get_jwt_identity()
        # registrar_en_bitacora(usuario_id, "actualizar", "actualizando movimiento")

        db.session.commit()
        return jsonify(movimiento_schema.dump(movimiento)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un movimiento
@movimiento_bp.route('/movimientos/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_movimiento(id):
    try:
        movimiento = Movimiento.query.get_or_404(id)  # Buscar el movimiento por ID
        db.session.delete(movimiento)  # Eliminar el movimiento
        
        movimiento = movimiento_schema.dump(movimiento)
        
        db.session.commit()
        return jsonify({'message': 'Movimiento eliminado', 'movimiento': movimiento}), 200  # Devolver el movimiento eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
