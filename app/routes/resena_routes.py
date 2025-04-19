from flask import Blueprint, request, jsonify
from ..models.resena_model import Resena
from ..schemas.resena_schema import ResenaSchema
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from ..utils.IdProductoUtils import producto_id
from ..utils.IdUsuarioUtils import cliente_id
from ..utils.RegisterBitacoraUtils import registrar_en_bitacora
from datetime import datetime

resena_bp = Blueprint('resena_bp', __name__)
resena_schema = ResenaSchema(session=db.session)
resenas_schema = ResenaSchema(many=True, session=db.session)

# Obtener todas las reseñas
@resena_bp.route('/resenas', methods=['GET'])
@jwt_required()
@cross_origin()
def get_resenas():
    try:
        resenas = Resena.query.all()    
        return jsonify(resenas_schema.dump(resenas))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una reseña por ID
@resena_bp.route('/resenas/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_resena(id):
    try:
        resena = Resena.query.get_or_404(id)
        return jsonify(resena_schema.dump(resena))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear una nueva reseña
@resena_bp.route('/resenas', methods=['POST'])
@jwt_required()
@cross_origin()
def add_resena():
    try:
        # print("Hola")
        data = request.get_json()
        
        # print(f"datos que hay hasta ahurita: {data}")
        data = cliente_id(data)
        data = producto_id(data)
        data["fecha"] = datetime.now().date().isoformat()
        
        nueva_resena = resena_schema.load(data)
        db.session.add(nueva_resena)
        db.session.commit()
        resena = resena_schema.dump(nueva_resena)
        
        return jsonify(resena), 201
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500

# Actualizar una reseña existente
@resena_bp.route('/resenas/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_resena(id):
    try:
        resena = Resena.query.get_or_404(id)
        
        resena_data = resena_schema.load(request.json, partial=True)

        for key in request.json:        
            setattr(resena, key, getattr(resena_data, key))
        
        
        db.session.commit()
        resena_actualizada = resena_schema.dump(resena)
        
        return jsonify(resena_actualizada)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una reseña
@resena_bp.route('/resenas/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_resena(id):
    try:
        resena = Resena.query.get_or_404(id)
        db.session.delete(resena)
        
        resena_eliminada = resena_schema.dump(resena)
        
        db.session.commit()
        return jsonify({'message': 'Reseña eliminada', 'data': resena_eliminada}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500