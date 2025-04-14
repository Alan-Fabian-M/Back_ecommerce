from flask import Blueprint, request, jsonify
from ..models.marca_model import Marca
from ..schemas.marca_schema import MarcaSchema
from app import db  # Asegúrate de importar db desde tu archivo de configuración
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

marca_bp = Blueprint('marca_bp', __name__)
marca_schema = MarcaSchema(session=db.session)
marcas_schema = MarcaSchema(many=True)

# Obtener todas las marcas
@marca_bp.route('/marcas', methods=['GET'])
@jwt_required()
@cross_origin()
def get_marcas():
    try:
        marcas = Marca.query.all()
        return jsonify(marcas_schema.dump(marcas))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una marca por ID
@marca_bp.route('/marcas/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_marca(id):
    try:
        marca = Marca.query.get_or_404(id)
        return jsonify(marca_schema.dump(marca))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@marca_bp.route('/marcas/<string:nombre>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_marca_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        marcas = Marca.query.filter(marca.nombre.ilike(f"%{nombre}%")).all()
        
        if not marcas:
            return jsonify({"error": f"No se encontraron marcas con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(marcas_schema.dump(marcas))
    except Exception as e:
        return jsonify({"error": f"Error al obtener marcas con nombre que contenga '{nombre}': {str(e)}"}), 500




# Crear una nueva marca
@marca_bp.route('/marcas', methods=['POST'])
@jwt_required()
@cross_origin()
def add_marca():
    try:
        # data = marca_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        data = marca_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        # nueva_marca = Marca(**data)  # Crear una nueva instancia de Marca
        db.session.add(data)
        db.session.commit()
        return jsonify(marca_schema.dump(data)), 201  # Devolver la marca creada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar una marca existente
@marca_bp.route('/marcas/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_marca(id):
    try:
        marca = Marca.query.get_or_404(id)  # Buscar la marca por ID
        data = request.get_json()  # Cargar los nuevos datos
        for key, value in data.items():
            setattr(marca, key, value)  # Actualizar los campos de la marca
        db.session.commit()
        return jsonify(marca_schema.dump(marca))  # Devolver la marca actualizada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una marca
@marca_bp.route('/marcas/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_marca(id):
    try:
        marca = Marca.query.get_or_404(id)  # Buscar la marca por ID
        db.session.delete(marca)  # Eliminar la marca
        db.session.commit()
        return jsonify({'message': 'Marca eliminada', 'data': marca_schema.dump(marca)}), 200  # Devolver la marca eliminada
    except Exception as e:
        return jsonify({"error": str(e)}), 500
