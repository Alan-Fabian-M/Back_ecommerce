from flask import Blueprint, request, jsonify
from ..models.rol_model import Rol
from ..schemas.rol_schema import RolSchema
from flask_jwt_extended import jwt_required
from app import db
from flask_cors import cross_origin

rol_bp = Blueprint('rol_bp', __name__)
rol_schema = RolSchema(session=db.session)
roles_schema = RolSchema(many=True)

# Función para serializar un rol

@rol_bp.route('/roles', methods=['GET'])
@jwt_required()
@cross_origin()
def get_roles():
    try:
        roles = Rol.query.all()
        return jsonify(roles_schema.dump(roles))  # Usa rol_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener los roles: {str(e)}"}), 500
    
    

@rol_bp.route('/roles/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_rol(id):
    try:
        rol = Rol.query.get_or_404(id)
        return jsonify(rol_schema.dump(rol))
    except Exception as e:
        return jsonify({"error": f"Error al obtener el rol con id {id}: {str(e)}"}), 500
    

@rol_bp.route('/roles', methods=['POST'])
@jwt_required()
@cross_origin()
def add_rol():
    try:
        # Load the data into the schema
        data = request.json
        if not all(key in data for key in ("nombre", "descripcion")):  # Verifica que los campos obligatorios estén presentes
            return jsonify({"error": "Campos 'nombre' y 'descripcion' son obligatorios"}), 400

        nuevo_rol = rol_schema.load(data)  # Deserialize data into Rol instance
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify(rol_schema.dump(nuevo_rol)), 201  # Devuelve el objeto serializado
    except Exception as e:
        return jsonify({"error": f"Error al crear el rol: {str(e)}"}), 500

@rol_bp.route('/roles/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_rol(id):
    try:
        rol = Rol.query.get_or_404(id)

        data = rol_schema.load(request.get_json(), partial=True)
        for key in request.json:
            setattr(rol, key, getattr(data, key))

        db.session.commit()
        return jsonify(rol_schema.dump(rol)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el rol con id {id}: {str(e)}"}), 500


@rol_bp.route('/roles/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_rol(id):
    try:
        rol = Rol.query.get_or_404(id)
        db.session.delete(rol)
        db.session.commit()
        return jsonify({'message': 'Rol eliminado'}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el rol con id {id}: {str(e)}"}), 500


@rol_bp.route('/roles/<string:nombre>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_rol_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        roles = Rol.query.filter(Rol.nombre.ilike(f"%{nombre}%")).all()
        
        if not roles:
            return jsonify({"error": f"No se encontraron roles con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(roles_schema.dump(roles))
    except Exception as e:
        return jsonify({"error": f"Error al obtener roles con nombre que contenga '{nombre}': {str(e)}"}), 500
