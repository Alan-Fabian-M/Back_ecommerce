from ..models.usuario_model import Usuario
from ..schemas.usuario_schema import UsuarioSchema
from flask import Blueprint, request, jsonify
from app import db

usuario_bp = Blueprint('usuario_bp', __name__)
usuario_schema = UsuarioSchema(session=db.session)
usuarios_schema = UsuarioSchema(many=True)

# Función para serializar un usuario
def usuario_to_dict(usuario):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,  # Asumiendo que Usuario tiene un campo 'nombre'
        "gmail": usuario.gmail,  # Asumiendo que Usuario tiene un campo 'email'
        "rol_id": usuario.rol_id  # Asumiendo que Usuario tiene un campo 'rol_id'
    }

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify(usuarios_schema.dump(usuarios))  # Usa usuario_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener los usuarios: {str(e)}"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        return jsonify(usuario_schema.dump(usuario))  # Usa usuario_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener el usuario con id {id}: {str(e)}"}), 500

@usuario_bp.route('/usuarios', methods=['POST'])
def add_usuario():
    try:
        # Verifica que los campos obligatorios estén presentes
        # data = request.json
        # if not all(key in data for key in ("nombre", "email", "rol_id")):
        #     return jsonify({"error": "Los campos 'nombre', 'email' y 'rol_id' son obligatorios"}), 400
        
        # Deserializa los datos
        # nuevo_usuario = usuario_schema.load(data)
        # db.session.add(nuevo_usuario)
        # db.session.commit()
        # return jsonify(usuario_to_dict(nuevo_usuario)), 201  # Devuelve el usuario serializado
    
        nuevo_usuario = usuario_schema.load(request.json)  # Ya es una instancia de usuario
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(usuario_schema.dump(nuevo_usuario)), 201 
    except Exception as e:
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        data = request.json

        # Verifica que al menos un campo se haya proporcionado para la actualización
        if not any(data.values()):
            return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400
        
        # Deserializa y actualiza los campos proporcionados
        updated_data = usuario_schema.load(data, partial=True)
        for key, value in updated_data.items():
            setattr(usuario, key, value)
        db.session.commit()
        return jsonify(usuario_to_dict(usuario))  # Devuelve el usuario actualizado
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el usuario con id {id}: {str(e)}"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado'}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el usuario con id {id}: {str(e)}"}), 500
