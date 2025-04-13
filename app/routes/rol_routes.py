from flask import Blueprint, request, jsonify
from ..models.rol_model import Rol
from ..schemas.rol_schema import RolSchema
from flask_jwt_extended import jwt_required
from app import db

rol_bp = Blueprint('rol_bp', __name__)
rol_schema = RolSchema(session=db.session)
roles_schema = RolSchema(many=True)

# Función para serializar un rol
def rol_to_dict(rol):
    return {
        "id": rol.id,
        "nombre": rol.nombre,  # Asumiendo que Rol tiene un campo 'nombre'
        "descripcion": rol.descripcion  # Asumiendo que Rol tiene un campo 'descripcion'
    }

@rol_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    try:
        roles = Rol.query.all()
        return jsonify(roles_schema.dump(roles))  # Usa rol_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener los roles: {str(e)}"}), 500
    
    

@rol_bp.route('/roles/<int:id>', methods=['GET'])
@jwt_required()
def get_rol(id):
    try:
        rol = Rol.query.get_or_404(id)
        return jsonify(rol_schema.dump(rol))
    except Exception as e:
        return jsonify({"error": f"Error al obtener el rol con id {id}: {str(e)}"}), 500
    
    

@rol_bp.route('/roles', methods=['POST'])
@jwt_required()
def add_rol():
    try:
        # Load the data into the schema
        data = request.json
        if not all(key in data for key in ("nombre", "descripcion")):  # Verifica que los campos obligatorios estén presentes
            return jsonify({"error": "Campos 'nombre' y 'descripcion' son obligatorios"}), 400

        nuevo_rol = rol_schema.load(data)  # Deserialize data into Rol instance
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify(rol_to_dict(nuevo_rol)), 201  # Devuelve el objeto serializado
    except Exception as e:
        return jsonify({"error": f"Error al crear el rol: {str(e)}"}), 500

@rol_bp.route('/roles/<int:id>', methods=['PUT'])
@jwt_required()
def update_rol(id):
    try:
        rol = Rol.query.get_or_404(id)
        data = request.json
        if not any(data.values()):  # Verifica que al menos un campo sea proporcionado
            return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400
        
        # Carga los datos, permitiendo campos opcionales
        updated_data = rol_schema.load(data, partial=True)
        for key, value in updated_data.items():
            setattr(rol, key, value)  # Actualiza los atributos
        db.session.commit()
        return jsonify(rol_to_dict(rol))  # Devuelve el objeto actualizado serializado
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el rol con id {id}: {str(e)}"}), 500

@rol_bp.route('/roles/<int:id>', methods=['DELETE'])
@jwt_required()
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
def get_rol_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        roles = Rol.query.filter(Rol.nombre.ilike(f"%{nombre}%")).all()
        
        if not roles:
            return jsonify({"error": f"No se encontraron roles con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(roles_schema.dump(roles))
    except Exception as e:
        return jsonify({"error": f"Error al obtener roles con nombre que contenga '{nombre}': {str(e)}"}), 500
