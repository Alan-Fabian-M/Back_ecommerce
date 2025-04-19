from datetime import datetime
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

        # if not all(k in data for k in ("cliente_id", "metodo_pago_id", "fecha", "total")):
        #     return jsonify({"error": "Faltan campos requeridos: cliente_id, metodo_pago_id, fecha, total"}), 400

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
        
        
        
        
        for key in request.json:
            setattr(venta, key, getattr(data, key))

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
