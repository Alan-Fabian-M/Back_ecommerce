from flask import Blueprint, request, jsonify
from ..models.cliente_model import Cliente
from ..schemas.cliente_schema import ClienteSchema
from app import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

cliente_bp = Blueprint('cliente_bp', __name__)
cliente_schema = ClienteSchema(session=db.session)
clientes_schema = ClienteSchema(many=True)

# Obtener todos los clientes
@cliente_bp.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        clientes = Cliente.query.all()
        return jsonify(clientes_schema.dump(clientes))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un cliente por ID
@cliente_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    try:
        cliente = Cliente.query.get_or_404(id)
        return jsonify(cliente_schema.dump(cliente))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cliente_bp.route('/clientes/<string:nombre>', methods=['GET'])
def get_cliente_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        clientes = Cliente.query.filter(Cliente.nombre.ilike(f"%{nombre}%")).all()
        
        if not clientes:
            return jsonify({"error": f"No se encontraron clientes con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(clientes_schema.dump(clientes))
    except Exception as e:
        return jsonify({"error": f"Error al obtener clientes con nombre que contenga '{nombre}': {str(e)}"}), 500


# Crear un nuevo cliente
@cliente_bp.route('/clientes', methods=['POST'])
def add_cliente():
    try:
        data = request.json
        data['contrasena'] = generate_password_hash(data['contrasena'])
        
        nuevo_cliente = cliente_schema.load(data)
        
        db.session.add(nuevo_cliente)
        db.session.commit()         
        
        return jsonify(cliente_schema.dump(nuevo_cliente)), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear el cliente: {str(e)}"}), 500



@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_cliente(id):
    try:
        cliente = Cliente.query.get_or_404(id)

        data = request.json


        # data = cliente_schema.load(request.get_json(), partial=True)
        
        for key, value in data.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)

        db.session.commit()
        return jsonify(cliente_schema.dump(cliente)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Eliminar un cliente
@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        cliente = Cliente.query.get_or_404(id)  # Buscar el cliente por ID
        db.session.delete(cliente)  # Eliminar el cliente
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado', 'data': cliente_schema.dump(cliente)}), 200  # Devolver el cliente eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
