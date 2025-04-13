from flask import Blueprint, jsonify, request
from app import db
from ..models.producto_model import Producto  # Asegúrate de importar el modelo correcto
from ..schemas.producto_schema import ProductoSchema
from flask_jwt_extended import jwt_required

producto_bp = Blueprint('producto', __name__)
Producto_schema = ProductoSchema(session=db.session)
Productos_schema = ProductoSchema(many=True)

# Función para serializar un producto
def producto_to_dict(producto):
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "stock": producto.stock,
        "precio": str(producto.precio),
        "descripcion": producto.descripcion
    }

# Obtener todos los productos
@producto_bp.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    try:
        productos = Producto.query.all()  # Obtener todos los productos
        return jsonify(Productos_schema.dump(productos))
    except Exception as e:
        return jsonify({"error": f"Error al obtener los productos: {str(e)}"}), 500

# Obtener un producto específico por ID
@producto_bp.route('/productos/<int:id>', methods=['GET'])
@jwt_required()
def get_producto(id):
    try:
        producto = Producto.query.get_or_404(id)  # Obtener el producto por ID
        return jsonify(Producto_schema.dump(producto))
    except Exception as e:
        return jsonify({"error": f"Error al obtener el producto con id {id}: {str(e)}"}), 500

# Crear un nuevo producto
# @producto_bp.route('/productos', methods=['POST'])
# def create_producto():
#     try:
#         data = request.json
#         # Validar que los campos requeridos estén presentes
#         if not all(key in data for key in ("nombre", "stock", "precio", "descripcion")):
#             return jsonify({"error": "Faltan campos requeridos"}), 400

#         producto = Producto(**data)  # Crear el nuevo producto con los datos recibidos
#         db.session.add(producto)  # Agregar el producto a la base de datos
#         db.session.commit()  # Confirmar la transacción
#         return jsonify({"mensaje": "Producto creado correctamente", "producto": producto_to_dict(producto)}), 201
#     except Exception as e:
#         return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 400

@producto_bp.route('/productos', methods=['POST'])
@jwt_required()
def create_producto():
    try:
        data = request.json
        # Validar que los campos requeridos estén presentes
        if not all(key in data for key in ("nombre", "stock", "precio", "descripcion", "categoria_nombre", "marca_nombre")):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Crear el nuevo producto con los datos recibidos, incluyendo los nombres de la categoría y la marca
        producto = Producto_schema.load(data)  # Esto ahora convierte los nombres en ids

        db.session.add(producto)  # Agregar el producto a la base de datos
        db.session.commit()  # Confirmar la transacción
        return jsonify({"mensaje": "Producto creado correctamente", "producto": producto_to_dict(producto)}), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 400

# Actualizar un producto existente
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
@jwt_required()
def update_producto(id):
    try:
        producto = Producto.query.get_or_404(id)  # Obtener el producto a actualizar
        data = request.json

        # Validar que los campos requeridos estén presentes
        if not all(key in data for key in ("nombre", "stock", "precio", "descripcion")):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Actualizar los atributos del producto
        for key, value in data.items():
            setattr(producto, key, value)
        db.session.commit()  # Confirmar la transacción
        return jsonify({"mensaje": "Producto actualizado correctamente", "producto": producto_to_dict(producto)})
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto con id {id}: {str(e)}"}), 400

# Eliminar un producto
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_producto(id):
    try:
        producto = Producto.query.get_or_404(id)  # Obtener el producto a eliminar
        db.session.delete(producto)  # Eliminar el producto de la base de datos
        db.session.commit()  # Confirmar la transacción
        return jsonify({"mensaje": "Producto eliminado correctamente", "producto": producto_to_dict(producto)})
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el producto con id {id}: {str(e)}"}), 500
