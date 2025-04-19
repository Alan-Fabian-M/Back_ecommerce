from ..utils.IdCategoriaUtils import categoria_id
from ..utils.IdMarcaUtils import marca_id
from flask import Blueprint, jsonify, request
from app import db
from ..models.producto_model import Producto  # Asegúrate de importar el modelo correcto
from ..schemas.producto_schema import ProductoSchema
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

producto_bp = Blueprint('producto', __name__)
Producto_schema = ProductoSchema(session=db.session)
Productos_schema = ProductoSchema(many=True)

# Función para serializar un producto

# Obtener todos los productos
@producto_bp.route('/productos', methods=['GET'])
@jwt_required()
@cross_origin()
def get_productos():
    try:
        productos = Producto.query.all()  # Obtener todos los productos
        return jsonify(Productos_schema.dump(productos))
    except Exception as e:
        return jsonify({"error": f"Error al obtener los productos: {str(e)}"}), 500

# Obtener un producto específico por ID
@producto_bp.route('/productos/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_producto(id):
    try:
        producto = Producto.query.get_or_404(id)  # Obtener el producto por ID
        return jsonify(Producto_schema.dump(producto))
    except Exception as e:
        return jsonify({"error": f"Error al obtener el producto con id {id}: {str(e)}"}), 500

@producto_bp.route('/productos/<string:nombre>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_producto_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        productos = Producto.query.filter(Producto.nombre.ilike(f"%{nombre}%")).all()
        
        if not productos:
            return jsonify({"error": f"No se encontraron productoes con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(Productos_schema.dump(productos))
    except Exception as e:
        return jsonify({"error": f"Error al obtener productoes con nombre que contenga '{nombre}': {str(e)}"}), 500


@producto_bp.route('/productos', methods=['POST'])
@jwt_required()
@cross_origin()
def create_producto():
    try:
        data = request.get_json()
        # Validar que los campos requeridos estén presentes
        # if not all(key in data for key in ("nombre", "stock", "precio", "descripcion", "categoria_nombre", "marca_nombre")):
        #     return jsonify({"error": "Faltan campos requeridos"}), 400

        # Crear el nuevo producto con los datos recibidos, incluyendo los nombres de la categoría y la marca
        data = marca_id(data)
        data = categoria_id(data)
        producto = Producto_schema.load(data)  # Esto ahora convierte los nombres en ids

        db.session.add(producto)  # Agregar el producto a la base de datos
        db.session.commit()  # Confirmar la transacción
        nuevo_producto = Producto_schema.dump(producto)
        print("Hola")
        return jsonify(nuevo_producto), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 400

# Actualizar un producto existente
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_producto(id):
    try:
        producto = Producto.query.get_or_404(id)

        data = request.get_json()
        
        data = marca_id(data)
        data = categoria_id(data)

        data = Producto_schema.load(request.get_json(), partial=True)
        for key in request.json:
            setattr(producto, key, getattr(data, key))

        db.session.commit()
        return jsonify(Producto_schema.dump(producto)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar el producto con id {id}: {str(e)}"}), 500


# # Eliminar un producto
# @producto_bp.route('/productos/<int:id>', methods=['DELETE'])
# @jwt_required()
# @cross_origin()
# def delete_producto(id):
#     try:
#         producto = Producto.query.get_or_404(id)  # Obtener el producto a eliminar
#         db.session.delete(producto)  # Eliminar el producto de la base de datos
#         db.session.commit()  # Confirmar la transacción
#         return jsonify({"mensaje": "Producto eliminado correctamente", "producto": producto_to_dict(producto)})
#     except Exception as e:
#         return jsonify({"error": f"Error al eliminar el producto con id {id}: {str(e)}"}), 500
