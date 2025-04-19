from ..utils.uploader import subir_imagen
from ..models.categoria_model import Categoria
from ..schemas.categoria_schema import CategoriaSchema
from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

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

@categoria_bp.route('/categorias/<string:nombre>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_categoria_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        categorias = Categoria.query.filter(Categoria.nombre.ilike(f"%{nombre}%")).all()
        
        if not categorias:
            return jsonify({"error": f"No se encontraron categoriaes con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(categorias_schema.dump(categorias))
    except Exception as e:
        return jsonify({"error": f"Error al obtener categoriaes con nombre que contenga '{nombre}': {str(e)}"}), 500



# Crear una nueva categoría
@categoria_bp.route('/categorias', methods=['POST'])
@jwt_required()
@cross_origin()
def add_categoria():
    try:
        data = categoria_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        archivo = request.files.get("imagen") 
        
        if archivo:
            url = subir_imagen(archivo)
            data["url"] = url
        
        
        db.session.add(data)
        
        db.session.flush()  # consigue el ID sin hacer commit



        db.session.commit()
        return jsonify(categoria_schema.dump(data)), 201  # Devolver la categoría creada
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_categoria(id):
    try:
        categoria = Categoria.query.get_or_404(id)
        archivo = request.files.get("imagen")

        if archivo:
            url = subir_imagen(archivo)
            data["url"] = url  # Actualiza la URL de la imagen

        
        data = categoria_schema.load(request.get_json(), partial=True)
        for key in request.json:
            setattr(categoria, key, getattr(data, key))

        db.session.commit()
        return jsonify(categoria_schema.dump(categoria)), 200
    except Exception as e:
        db.session.rollback()
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
