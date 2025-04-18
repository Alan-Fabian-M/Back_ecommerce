from ..models.bitacora_model import Bitacora
from ..schemas.bitacora_schema import BitacoraSchema
from flask import Blueprint, request, jsonify
from app import db
from flask_cors import cross_origin

bitacora_bp = Blueprint('bitacora_bp', __name__)
bitacora_schema = BitacoraSchema(session=db.session)
bitacoras_schema = BitacoraSchema(many=True)

# Obtener todas las bitácoras
@bitacora_bp.route('/bitacoras', methods=['GET'])
@cross_origin()
def get_bitacoras():
    try:
        bitacoras = Bitacora.query.all()
        return jsonify(bitacoras_schema.dump(bitacoras))  # Usamos dump() para convertirlo en JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una bitácora por ID
@bitacora_bp.route('/bitacoras/<int:id>', methods=['GET'])
@cross_origin()
def get_bitacora(id):
    try:
        bitacora = Bitacora.query.get_or_404(id)
        return jsonify(bitacora_schema.dump(bitacora))  # Usamos dump() para convertirlo en JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear una nueva bitácora
@bitacora_bp.route('/bitacoras', methods=['POST'])
@cross_origin()
def add_bitacora():
    try:
        data = bitacora_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        nueva_bitacora = Bitacora(**data)
        db.session.add(nueva_bitacora)
        db.session.commit()
        return jsonify(bitacora_schema.dump(nueva_bitacora)), 201  # Usar dump() y devolver el objeto recién creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar una bitácora existente
@bitacora_bp.route('/bitacoras/<int:id>', methods=['PUT'])
@cross_origin()
def update_bitacora(id):
    try:
        bitacora = Bitacora.query.get_or_404(id)  # Si no existe, devuelve un error 404
        data = bitacora_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        for key, value in data.items():
            setattr(bitacora, key, value)  # Actualizar los atributos de la bitácora
        db.session.commit()
        return jsonify(bitacora_schema.dump(bitacora))  # Retornar el objeto actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una bitácora
@bitacora_bp.route('/bitacoras/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_bitacora(id):
    try:
        bitacora = Bitacora.query.get_or_404(id)
        db.session.delete(bitacora)
        db.session.commit()
        return jsonify({'message': 'Bitacora eliminada'}), 200  # Respuesta exitosa
    except Exception as e:
        return jsonify({"error": str(e)}), 500
