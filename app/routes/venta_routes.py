from ..models.venta_model import Venta
from ..schemas.venta_schema import VentaSchema
from flask import Blueprint, request, jsonify
from app import db

venta_bp = Blueprint('venta_bp', __name__)
venta_schema = VentaSchema(session=db.session)
ventas_schema = VentaSchema(many=True)

@venta_bp.route('/ventas', methods=['GET'])
def get_ventas():
    try:
        ventas = Venta.query.all()
        return jsonify(ventas_schema.dump(ventas)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las ventas: {str(e)}"}), 500

@venta_bp.route('/ventas/<int:id>', methods=['GET'])
def get_venta(id):
    try:
        venta = Venta.query.get_or_404(id)
        return jsonify(venta_schema.dump(venta)), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener la venta: {str(e)}"}), 500

@venta_bp.route('/ventas', methods=['POST'])
def add_venta():
    try:
        data = request.json

        # Validación básica (ajusta según tu modelo)
        if not all(k in data for k in ("cliente_id", "metodo_pago_id", "fecha", "total")):
            return jsonify({"error": "Faltan campos requeridos: cliente_id, metodo_pago_id, fecha, total"}), 400

        nueva_venta = venta_schema.load(data)
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify(venta_schema.dump(nueva_venta)), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar la venta: {str(e)}"}), 500

@venta_bp.route('/ventas/<int:id>', methods=['PUT'])
def update_venta(id):
    try:
        venta = Venta.query.get_or_404(id)
        data = venta_schema.load(request.json, partial=True)  # Permite actualización parcial

        for key, value in data.items():
            setattr(venta, key, value)

        db.session.commit()
        return jsonify(venta_schema.dump(venta)), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la venta: {str(e)}"}), 500

@venta_bp.route('/ventas/<int:id>', methods=['DELETE'])
def delete_venta(id):
    try:
        venta = Venta.query.get_or_404(id)
        db.session.delete(venta)
        db.session.commit()
        return jsonify({'message': 'Venta eliminada'}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la venta: {str(e)}"}), 500
