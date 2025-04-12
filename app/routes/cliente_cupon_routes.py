from ..models.cliente_cupon_model import ClienteCupon
from ..schemas.cliente_cupon_schema import ClienteCuponSchema
from flask import Blueprint, request, jsonify
from app import db

cliente_cupon_bp = Blueprint('cliente_cupon_bp', __name__)
cliente_cupon_schema = ClienteCuponSchema(session=db.session)
cliente_cupons_schema = ClienteCuponSchema(many=True)

# Obtener todos los cliente-cupones
@cliente_cupon_bp.route('/cliente_cupons', methods=['GET'])
def get_cliente_cupons():
    try:
        cliente_cupons = ClienteCupon.query.all()
        return jsonify(cliente_cupons_schema.dump(cliente_cupons))  # Usamos dump() para convertir a JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo cliente-cupon
@cliente_cupon_bp.route('/cliente_cupons', methods=['POST'])
def add_cliente_cupon():
    try:
        data = cliente_cupon_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        nuevo_cliente_cupon = ClienteCupon(**data)
        db.session.add(nuevo_cliente_cupon)
        db.session.commit()
        return jsonify(cliente_cupon_schema.dump(nuevo_cliente_cupon)), 201  # Devolver el objeto creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un cliente-cupon por cliente_id y cupon_id
@cliente_cupon_bp.route('/cliente_cupons/<int:cliente_id>/<int:cupon_id>', methods=['DELETE'])
def delete_cliente_cupon(cliente_id, cupon_id):
    try:
        cliente_cupon = ClienteCupon.query.get_or_404((cliente_id, cupon_id))  # Buscar el cliente-cupon por ID
        db.session.delete(cliente_cupon)
        db.session.commit()
        return jsonify({'message': 'Cliente-Cupon eliminado', 'data': cliente_cupon_schema.dump(cliente_cupon)}), 200  # Devolver el objeto eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
