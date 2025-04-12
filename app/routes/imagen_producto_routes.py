from flask import Blueprint, request, jsonify
from ..models.imagen_producto_model import ImagenProducto
from ..schemas.imagen_producto_schema import ImagenProductoSchema
from app import db

imagen_producto_bp = Blueprint('imagen_producto_bp', __name__)
imagen_producto_schema = ImagenProductoSchema(session=db.session)
imagenes_producto_schema = ImagenProductoSchema(many=True)

# Obtener todas las imágenes de productos
@imagen_producto_bp.route('/imagenes_producto', methods=['GET'])
def get_imagenes_producto():
    try:
        imagenes = ImagenProducto.query.all()
        return jsonify(imagenes_producto_schema.dump(imagenes))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una imagen de producto por ID
@imagen_producto_bp.route('/imagenes_producto/<int:id>', methods=['GET'])
def get_imagen_producto(id):
    try:
        imagen = ImagenProducto.query.get_or_404(id)
        return jsonify(imagen_producto_schema.dump(imagen))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear una nueva imagen de producto
@imagen_producto_bp.route('/imagenes_producto', methods=['POST'])
def add_imagen_producto():
    try:
        data = imagen_producto_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        nueva_imagen = ImagenProducto(**data)  # Crear una nueva instancia de ImagenProducto
        db.session.add(nueva_imagen)
        db.session.commit()
        return jsonify(imagen_producto_schema.dump(nueva_imagen)), 201  # Devolver la imagen creada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar una imagen de producto existente
@imagen_producto_bp.route('/imagenes_producto/<int:id>', methods=['PUT'])
def update_imagen_producto(id):
    try:
        imagen = ImagenProducto.query.get_or_404(id)  # Buscar la imagen por ID
        data = imagen_producto_schema.load(request.json)  # Cargar los nuevos datos
        for key, value in data.items():
            setattr(imagen, key, value)  # Actualizar los campos de la imagen
        db.session.commit()
        return jsonify(imagen_producto_schema.dump(imagen))  # Devolver la imagen actualizada
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una imagen de producto
@imagen_producto_bp.route('/imagenes_producto/<int:id>', methods=['DELETE'])
def delete_imagen_producto(id):
    try:
        imagen = ImagenProducto.query.get_or_404(id)  # Buscar la imagen por ID
        db.session.delete(imagen)  # Eliminar la imagen
        db.session.commit()
        return jsonify({'message': 'Imagen del producto eliminada', 'data': imagen_producto_schema.dump(imagen)}), 200  # Devolver la imagen eliminada
    except Exception as e:
        return jsonify({"error": str(e)}), 500
