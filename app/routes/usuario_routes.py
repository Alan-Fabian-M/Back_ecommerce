from ..utils.IdRolUtils import rol_id
from ..models.usuario_model import Usuario
from ..schemas.usuario_schema import UsuarioSchema
from ..models.rol_model import Rol  
from flask import Blueprint, request, jsonify
from app import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin


usuario_bp = Blueprint('usuario_bp', __name__)
usuario_schema = UsuarioSchema(session=db.session)
usuarios_schema = UsuarioSchema(many=True)


@usuario_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@cross_origin()
def get_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify(usuarios_schema.dump(usuarios))  # Usa usuario_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener los usuarios: {str(e)}"}), 500


@usuario_bp.route('/usuarios/<string:nombre>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_usuario_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        usuarios = Usuario.query.filter(Usuario.nombre.ilike(f"%{nombre}%")).all()
        
        if not usuarios:
            return jsonify({"error": f"No se encontraron usuarios con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(usuarios_schema.dump(usuarios))
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuarios con nombre que contenga '{nombre}': {str(e)}"}), 500


@usuario_bp.route('/usuarios/rol/<string:nombre_rol>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_usuarios_por_nombre_rol(nombre_rol):
    try:
        # Buscar roles cuyo nombre coincida parcialmente con el texto recibido
        roles = Rol.query.filter(Rol.nombre.ilike(f"%{nombre_rol}%")).all()
        
        if not roles:
            return jsonify({"error": f"No se encontró ningún rol con nombre que contenga '{nombre_rol}'"}), 404

        # Extraer los IDs de esos roles
        rol_ids = [rol.id for rol in roles]

        # Buscar usuarios que tengan alguno de esos roles
        usuarios = Usuario.query.filter(Usuario.rol_id.in_(rol_ids)).all()

        if not usuarios:
            return jsonify({"error": f"No se encontraron usuarios con rol '{nombre_rol}'"}), 404

        return jsonify(usuarios_schema.dump(usuarios))
    
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuarios con rol '{nombre_rol}': {str(e)}"}), 500



@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        return jsonify(usuario_schema.dump(usuario))  # Usa usuario_to_dict para serializar
    except Exception as e:
        return jsonify({"error": f"Error al obtener el usuario con id {id}: {str(e)}"}), 500


@usuario_bp.route('/usuarios', methods=['POST'])
# @jwt_required()
@cross_origin()
def add_usuario():
    try:
        data = request.json
        rol_nombre = data.get("rol_nombre")  # Recibimos el nombre del rol en el JSON
        
        # Buscar el rol por nombre
        rol = Rol.query.filter_by(nombre=rol_nombre).first()
        if not rol:
            return jsonify({"error": f"El rol '{rol_nombre}' no existe."}), 400
        
        # Asignamos el id del rol al diccionario de datos
        data['rol_id'] = rol.id
        del data['rol_nombre']  # Eliminamos el campo 'rol_nombre' para que no se guarde
        data['contrasena'] = generate_password_hash(data['contrasena'])
        # Deserializamos y validamos los datos del nuevo usuario
        nuevo_usuario = usuario_schema.load(data)  # Usamos el esquema para validación y deserialización

        # Agregar el usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify(usuario_schema.dump(nuevo_usuario)), 201

    except Exception as e:
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500


@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        data = request.json

        if not any(data.values()):
            return jsonify({"error": "Debe proporcionar al menos un campo para actualizar"}), 400

        data = rol_id(data)

        # Actualizar campos uno por uno desde el dict
        for key, value in data.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        db.session.commit()
        return jsonify(usuario_schema.dump(usuario)), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error al actualizar el usuario con id {id}: {str(e)}"}), 500

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_usuario(id):
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado'}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el usuario con id {id}: {str(e)}"}), 500
    

    #Validar Correo 
@usuario_bp.route('/usuarios/validar-correo', methods=['POST'])
@cross_origin()
def validar_correo():
    gmail = request.json.get('gmail')
    if not gmail:
        return jsonify({"error": "Correo no proporcionado"}), 400

    usuario = Usuario.query.filter_by(gmail=gmail).first()
    return jsonify({"existe": usuario is not None})

