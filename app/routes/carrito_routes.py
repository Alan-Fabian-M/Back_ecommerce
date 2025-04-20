from ..models.cupon_model import Cupon
from ..models.producto_model import Producto
from ..models.venta_model import Venta
from ..models.carrito_model import Carrito
from ..schemas.carrito_schema import CarritoSchema
from flask import Blueprint, request, jsonify
from app import db

carrito_bp = Blueprint('carrito_bp', __name__)
carrito_schema = CarritoSchema(session=db.session)
carritos_schema = CarritoSchema(many=True)

# Obtener todos los carritos
@carrito_bp.route('/carritos', methods=['GET'])
def get_carritos():
    try:
        carritos = Carrito.query.all()
        return jsonify(carritos_schema.dump(carritos))  # Usamos dump() para convertir a JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un carrito por ID
@carrito_bp.route('/carritos/<int:id>', methods=['GET'])
def get_carrito(id):
    try:
        carrito = Carrito.query.get_or_404(id)  # Si no existe, devuelve un error 404
        return jsonify(carrito_schema.dump(carrito))  # Usamos dump() para convertir a JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@carrito_bp.route('/carritos', methods=['POST'])
def add_carrito():
    try:
        nuevo_carrito = carrito_schema.load(request.json)  # Cargar datos de la solicitud JSON
        
        venta = Venta.query.get(nuevo_carrito.venta_id)
        producto = Producto.query.get(nuevo_carrito.producto_id)

        # print("1234567890")
        
        db.session.add(nuevo_carrito)

        print(venta.importe_total)
        
        nuevo_carrito.precio = (producto.precio or 0)
        nuevo_carrito.importe = (nuevo_carrito.cantidad * nuevo_carrito.precio)
        venta.importe_total = (venta.importe_total or 0) + nuevo_carrito.importe


        print(venta.importe_total)
        db.session.commit()

        # Usamos el esquema para devolver la respuesta en formato JSON
        return jsonify(carrito_schema.dump(nuevo_carrito)), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500  


@carrito_bp.route('/carritos/<int:venta_id>/<int:producto_id>', methods=['PUT'])
def update_carrito(venta_id, producto_id):
    try:
        # Buscar el carrito que se quiere actualizar
        carrito = Carrito.query.get_or_404((venta_id, producto_id))
        
        # Guardamos los valores anteriores para calcular la diferencia de importe y cantidad
        old_cantidad = carrito.cantidad
        old_precio = carrito.precio or 0
        old_desc = carrito.importe_desc or 0

        
        # Cargar los nuevos datos desde la solicitud
        data = carrito_schema.load(request.json, partial=True) 

        # Actualizar los atributos del carrito
        for key in request.json:
            setattr(carrito, key, getattr(data, key))
        
        # Obtener la venta y el producto relacionados
        venta = Venta.query.get(venta_id)
        producto = Producto.query.get(producto_id)

        if not venta or not producto:
            return jsonify({"error": "Venta o Producto no encontrados"}), 400

        # Actualizamos la venta con los nuevos importes
        # Si la cantidad cambia, debemos ajustar los totales
        if carrito.cantidad != old_cantidad:
            # Actualizar stock del producto
            diferencia_cantidad = carrito.cantidad - old_cantidad

            # Actualizar los importes en la venta
            venta.importe_total = ((venta.importe_total or 0) - ((old_precio or 0) * (old_cantidad or 0))) + ((carrito.precio or 0) * (carrito.cantidad or 0))
            # venta.importe_total_desc = (venta.importe_total_desc or 0) - ((old_desc or 0) * (old_cantidad or 0)) + ((carrito.importe_desc or 0) * (carrito.cantidad or 0))
            # carrito.importe = ((producto.precio or 0) * (carrito.cantidad or 0))
        
        db.session.commit()

        # Devolver el carrito actualizado como respuesta
        return jsonify(carrito_schema.dump(carrito))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar un carrito
@carrito_bp.route('/carritos/<int:venta_id>/<int:producto_id>', methods=['DELETE'])
def delete_carrito(venta_id, producto_id):
    try:
        carrito = Carrito.query.get_or_404((venta_id, producto_id))

        # Si estaba vendido, se revierte su impacto

        venta = Venta.query.get(venta_id)
        producto = Producto.query.get(producto_id)

        if venta:
            venta.importe_total = (venta.importe_total or 0) - carrito.importe
        db.session.commit()

        db.session.delete(carrito)
        db.session.commit()
        return jsonify({'message': 'Carrito eliminado correctamente'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
