from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from app import db
from ..models.usuario_model import Usuario
from ..schemas.usuario_schema import UsuarioSchema

auth_bp = Blueprint('auth_bp', __name__)
usuario_schema = UsuarioSchema()

@auth_bp.route('/login', methods=['POST'])

def login():
    data = request.get_json()
    gmail = data.get("gmail")
    contrasena = data.get("contrasena")

    if not gmail or not contrasena:
        return jsonify({"error": "Gmail y contraseña son requeridos"}), 400

    usuario = Usuario.query.filter_by(gmail=gmail).first()

    # ✅ Comparación correcta con contraseña hasheada
    if not usuario or not check_password_hash(usuario.contrasena, contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Convertir a string el codigo del usuario antes de pasarlo al token
    access_token = create_access_token(identity=str(usuario.codigo))
    return jsonify({
        "token": access_token,
        "rol": usuario_schema.dump(usuario)["rol"]
    }), 200


@auth_bp.route('/verificar-token', methods=['GET'])
@jwt_required()
def verificar_token():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    return jsonify({"mensaje": "Token válido", "usuario": usuario_schema.dump(usuario)}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Aquí podrías realizar algún manejo adicional si quieres invalidar el token en el backend
    # Pero usualmente solo se elimina el token en el frontend
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200
