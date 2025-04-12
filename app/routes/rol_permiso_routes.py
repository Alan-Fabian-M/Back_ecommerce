from flask import Blueprint, jsonify, request
from app import db
from ..models.rol_permiso_model import RolPermiso
from ..schemas.rol_permiso_schema import RolPermisoSchema

rol_permiso_bp = Blueprint('rol_permiso_bp', __name__)
rol_permiso_schema = RolPermisoSchema(session=db.session)
roles_permisos_schema = RolPermisoSchema(many=True)

# Función para serializar un rol_permiso
def rol_permiso_to_dict(rol_permiso):
    return {
        "rol_id": rol_permiso.rol_id,
        "permiso_id": rol_permiso.permiso_id
    }

# Obtener todos los roles-permisos
@rol_permiso_bp.route('/roles_permisos', methods=['GET'])
def get_roles_permisos():
    try:
        roles_permisos = RolPermiso.query.all()  # Obtener todos los roles-permisos
        return jsonify(roles_permisos_schema.dump(roles_permisos))
    except Exception as e:
        return jsonify({"error": f"Error al obtener los roles-permisos: {str(e)}"}), 500

# Obtener uno de roles-permisos
@rol_permiso_bp.route('/roles_permisos/<int:rol_id>/<int:permiso_id>', methods=['GET'])
def get_rol_permiso(rol_id, permiso_id):
    try:
        rol_permiso = RolPermiso.query.get_or_404((rol_id, permiso_id))
        return jsonify(rol_permiso_to_dict(rol_permiso))
    except Exception as e:
        return jsonify({"error": f"Error al obtener el rol-permiso con rol_id {rol_id} y permiso_id {permiso_id}: {str(e)}"}), 500
    
# Crear un nuevo rol-permiso
@rol_permiso_bp.route('/roles_permisos', methods=['POST'])
def add_rol_permiso():
    try:

        data = rol_permiso_schema.load(request.json)
        # Validar que los campos requeridos estén presentes
        # if not all(key in data for key in ("rol_id", "permiso_id")):
        #     return jsonify({"error": "Faltan campos requeridos"}), 400

        # nuevo_rol_permiso = RolPermiso(**data)  # Crear el nuevo rol-permiso con los datos recibidos
        db.session.add(data)  # Agregar el rol-permiso a la base de datos
        # return "hola", 400
        db.session.commit()  # Confirmar la transacción
        return jsonify({"mensaje": "Rol-Permiso creado correctamente", "rol_permiso": rol_permiso_to_dict(data)}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el rol-permiso: {str(e)}"}), 400

# Actualizar un rol-permiso existente
@rol_permiso_bp.route('/roles_permisos/<int:rol_id>/<int:permiso_id>', methods=['PUT'])
def update_rol_permiso(rol_id, permiso_id):
    try:
        rol_permiso = RolPermiso.query.get_or_404((rol_id, permiso_id))  # Obtener por clave compuesta
        data = request.json

        # Validar que los campos requeridos estén presentes
        if not all(key in data for key in ("rol_id", "permiso_id")):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Actualizar los atributos (opcional si permitís cambiar los IDs, aunque no suele hacerse)
        rol_permiso.rol_id = data["rol_id"]
        rol_permiso.permiso_id = data["permiso_id"]

        db.session.commit()
        return jsonify({
            "mensaje": "Rol-Permiso actualizado correctamente",
            "rol_permiso": rol_permiso_to_dict(rol_permiso)
        })
    except Exception as e:
        return jsonify({
            "error": f"Error al actualizar el rol-permiso con rol_id {rol_id} y permiso_id {permiso_id}: {str(e)}"
        }), 400


# Eliminar un rol-permiso
@rol_permiso_bp.route('/roles_permisos/<int:rol_id>/<int:permiso_id>', methods=['DELETE'])
def delete_rol_permiso(rol_id, permiso_id):
    try:
        rol_permiso = RolPermiso.query.get_or_404((rol_id, permiso_id))  # Obtener por clave compuesta
        db.session.delete(rol_permiso)
        db.session.commit()
        return jsonify({
            "mensaje": "Rol-Permiso eliminado correctamente",
            "rol_permiso": rol_permiso_to_dict(rol_permiso)
        })
    except Exception as e:
        return jsonify({
            "error": f"Error al eliminar el rol-permiso con rol_id {rol_id} y permiso_id {permiso_id}: {str(e)}"
        }), 500

