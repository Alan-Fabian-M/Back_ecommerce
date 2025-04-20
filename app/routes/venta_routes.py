from datetime import datetime

from ..models.cupon_model import Cupon

from ..models.producto_model import Producto
from ..utils.IdMetodoPagoUtils import metodo_pago_id
from ..utils.IdUsuarioUtils import cliente_id
from ..utils.IdCuponUtils import cupon_id
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from ..models.venta_model import Venta
from ..schemas.venta_schema import VentaSchema
from app import db

venta_bp = Blueprint('venta_bp', __name__)
venta_schema = VentaSchema(session=db.session)
ventas_schema = VentaSchema(many=True, session=db.session)

# Obtener todas las ventas
@venta_bp.route('/ventas', methods=['GET'])
@jwt_required()
@cross_origin()
def get_ventas():
    try:
        ventas = Venta.query.all()
        return jsonify(ventas_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una venta por ID
@venta_bp.route('/ventas/<int:id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_venta(id):
    try:
        venta = Venta.query.get_or_404(id)
        return jsonify(venta_schema.dump(venta)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear una nueva venta
@venta_bp.route('/ventas', methods=['POST'])
@jwt_required()
@cross_origin()
def add_venta():
    try:
        data = request.get_json()

        data = cliente_id(data)
        data = metodo_pago_id(data)
        data = cupon_id(data)
        
        data["fecha"] = datetime.now().date().isoformat()
        
        

        nueva_venta = venta_schema.load(data)
        db.session.add(nueva_venta)
        db.session.commit()

        return jsonify(venta_schema.dump(nueva_venta)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Actualizar una venta existente
@venta_bp.route('/ventas/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_venta(id):
    try:
        venta = Venta.query.get_or_404(id)

        data = request.get_json()

        data = cliente_id(data)
        data = metodo_pago_id(data)
        data = cupon_id(data)

        data = venta_schema.load(data, partial=True)

        # Verificamos si se va a cambiar el estado a "confirmado"
        estado_anterior = venta.estado
        nuevo_estado = getattr(data, 'estado', estado_anterior)

        for key in request.json:
            setattr(venta, key, getattr(data, key))

        
        cupon_aplicado = None
        descuento = 0

        if data.get("cupon_id"):
            cupon_aplicado = Cupon.query.get(data["cupon_id"])
            if not cupon_aplicado:
                return jsonify({"error": "Cupon no válido"}), 400
            descuento = float(cupon_aplicado.monto or 0)  # Asumimos que es porcentaje (por ejemplo, 10 = 10%)

        # Suponemos que el total original ya está en el campo 'importe_total'
        importe_total = float(data.get("importe_total", 0))
        importe_total_desc = importe_total

        if descuento > 0:
            importe_total_desc = round(importe_total - descuento, 2)

        data["importe_total_desc"] = importe_total_desc
        

        # Si el estado cambia a "confirmado", descontar stock
        if estado_anterior != "confirmado" and nuevo_estado == "confirmado":
            for carrito in venta.carritos:
                producto = Producto.query.get(carrito.producto_id)
                if producto and carrito.cantidad:
                    if producto.stock >= carrito.cantidad:
                        producto.stock -= carrito.cantidad
                    else:
                        raise Exception(f"Stock insuficiente para el producto '{producto.nombre}'.")

        db.session.commit()
        return jsonify(venta_schema.dump(venta)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una venta
@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
@jwt_required()
@cross_origin()
def delete_venta(id):
    try:
        venta = Venta.query.get_or_404(id)
        db.session.delete(venta)
        venta_eliminada = venta_schema.dump(venta)
        db.session.commit()

        return jsonify({'message': 'Venta eliminada', 'data': venta_eliminada}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
