from ..utils.uploader import subir_imagen
from ..utils.IdCategoriaUtils import categoria_id
from ..utils.IdMarcaUtils import marca_id
from flask import Blueprint, jsonify, request
from app import db
from ..models.producto_model import Producto  # Asegúrate de importar el modelo correcto
from ..models.imagen_producto_model import ImagenProducto  # Asegúrate de importar el modelo correcto
from ..schemas.producto_schema import ProductoSchema
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

producto_bp = Blueprint('producto', __name__)
Producto_schema = ProductoSchema(session=db.session)
Productos_schema = ProductoSchema(many=True)

# Función para serializar un producto
@producto_bp.route('/productos', methods=['GET'])
@cross_origin()
def get_productos():
    try:
        productos = Producto.query.all()
        resultado = []

        for prod in productos:
            # Si hay imágenes, tomar la primera. Si no, None.
            imagen = prod.imagenes[0] if prod.imagenes else None

            producto_data = Producto_schema.dump(prod)
            producto_data['imagen_url'] = imagen.image_url if imagen else None

            resultado.append(producto_data)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener los productos: {str(e)}"}), 400
    
# Obtener un producto específico por ID
@producto_bp.route('/productos/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_producto(id):
    try:
        producto = Producto.query.get_or_404(id)

        # Obtener la primera imagen, si existe
        imagen = producto.imagenes[0] if producto.imagenes else None

        producto_data = Producto_schema.dump(producto)
        producto_data['imagen_url'] = imagen.image_url if imagen else None

        return jsonify(producto_data), 200

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
            return jsonify({"error": f"No se encontraron productos con nombre que contenga '{nombre}'"}), 404

        resultado = []
        for prod in productos:
            imagen = prod.imagenes[0] if prod.imagenes else None
            producto_data = Producto_schema.dump(prod)
            producto_data['imagen_url'] = imagen.image_url if imagen else None
            producto_data['imagen_id'] = imagen.id if imagen else None
            resultado.append(producto_data)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener productos con nombre que contenga '{nombre}': {str(e)}"}), 500


@producto_bp.route('/productos', methods=['POST'])
@jwt_required()
@cross_origin()
def create_producto():
    try:
        data = request.form.to_dict()
        imagenes = request.files.getlist('imagenes')

        data = marca_id(data)
        data = categoria_id(data)
        producto = Producto_schema.load(data)

        db.session.add(producto)
        db.session.flush()  # Obtener ID sin hacer commit

        imagen_url = None  # Inicializar

        for i, archivo in enumerate(imagenes):
            if archivo and archivo.filename != '':
                url = subir_imagen(archivo)
                nueva_imagen = ImagenProducto(
                    image_url=url,  # ← corregido: usar image_url, no url
                    producto_id=producto.id,
                )
                db.session.add(nueva_imagen)


        db.session.commit()
        nuevo_producto = Producto_schema.dump(producto)

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
        archivo = request.files.get("imagen")
        imagen_url = None
        
        data = request.form.to_dict()
        data = marca_id(data)
        data = categoria_id(data)
        data = Producto_schema.load(data, partial=True)

        for key in request.form.to_dict():
            setattr(producto, key, getattr(data, key))
            
        if archivo:
            url = subir_imagen(archivo)
            nueva_imagen = ImagenProducto(url=url, producto_id=producto.id)
            db.session.add(nueva_imagen)
            imagen_url = url

        db.session.commit()
        
        respuesta_producto = Producto_schema.dump(producto)
        if imagen_url:
            respuesta_producto['imagen_url'] = imagen_url
            
        return jsonify(respuesta_producto), 200
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
