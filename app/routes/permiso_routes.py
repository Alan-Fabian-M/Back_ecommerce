from flask import Blueprint, request, jsonify
from ..models.permiso_model import Permiso
from ..schemas.permiso_schema import PermisoSchema
from app import db  # Asegúrate de importar db desde tu archivo de configuración
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

permiso_bp = Blueprint('permiso_bp', __name__)
permiso_schema = PermisoSchema(session=db.session)
permisos_schema = PermisoSchema(many=True)

# Obtener todos los permisos
@permiso_bp.route('/permisos', methods=['GET'])
@jwt_required()
@cross_origin()
def get_permisos():
    try:
        permisos = Permiso.query.all()
        return jsonify(permisos_schema.dump(permisos))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un permiso por ID
@permiso_bp.route('/permisos/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_permiso(id):
    try:
        permiso = Permiso.query.get_or_404(id)
        return jsonify(permiso_schema.dump(permiso))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo permiso
@permiso_bp.route('/permisos', methods=['POST'])
@jwt_required()
@cross_origin()
def add_permiso():

    try:
        # data = permiso_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        # nuevo_permiso = Permiso(**data)  # Crear una nueva instancia de Permiso
        nuevo_permiso = permiso_schema.load(request.json)  # Ya es una instancia de Permiso
        db.session.add(nuevo_permiso)
        db.session.commit()
        return jsonify(permiso_schema.dump(nuevo_permiso)), 201  # Devolver el nuevo permiso creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un permiso existente
@permiso_bp.route('/permisos/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_permiso(id):
    try:
        permiso = Permiso.query.get_or_404(id)  # Buscar el permiso por ID
        data = permiso_schema.load(request.json)  # Cargar los nuevos datos
        for key, value in data.items():
            setattr(permiso, key, value)  # Actualizar los campos del permiso
        db.session.commit()
        return jsonify(permiso_schema.dump(permiso))  # Devolver el permiso actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un permiso
@permiso_bp.route('/permisos/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_permiso(id):
    try:
        permiso = Permiso.query.get_or_404(id)  # Buscar el permiso por ID
        db.session.delete(permiso)  # Eliminar el permiso
        db.session.commit()
        return jsonify({'message': 'Permiso eliminado', 'data': permiso_schema.dump(permiso)}), 200  # Devolver el permiso eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
