from ..models.categoria_model import Categoria
from ..schemas.categoria_schema import CategoriaSchema
from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required

categoria_bp = Blueprint('categoria_bp', __name__)
categoria_schema = CategoriaSchema(session=db.session)
categorias_schema = CategoriaSchema(many=True)

# Obtener todas las categorías
@categoria_bp.route('/categorias', methods=['GET'])
@jwt_required()
@cross_origin()
def get_categorias():
    try:
        categorias = Categoria.query.all()
        return jsonify(categorias_schema.dump(categorias))  # Usamos dump() para convertir a JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una categoría por ID
@categoria_bp.route('/categorias/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_categoria(id):
    try:
        categoria = Categoria.query.get_or_404(id)  # Si no existe, devuelve un error 404
        return jsonify(categoria_schema.dump(categoria))  # Usamos dump() para convertir a JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear una nueva categoría
@categoria_bp.route('/categorias', methods=['POST'])
@jwt_required()
@cross_origin()
def add_categoria():
    try:
        data = categoria_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        
        db.session.add(data)
        db.session.commit()
        return jsonify(categoria_schema.dump(data)), 201  # Devolver la categoría creada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar una categoría existente
@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_categoria(id):
    try:
        categoria = Categoria.query.get_or_404(id)  # Si no existe, devuelve un error 404
        data = categoria_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        for key, value in data.items():
            setattr(categoria, key, value)  # Actualizar los atributos de la categoría
        db.session.commit()
        return jsonify(categoria_schema.dump(categoria))  # Retornar la categoría actualizada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una categoría
@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_categoria(id):
    try:
        categoria = Categoria.query.get_or_404(id)
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'message': 'Categoría eliminada'}), 200  # Respuesta exitosa
    except Exception as e:
        return jsonify({"error": str(e)}), 500
