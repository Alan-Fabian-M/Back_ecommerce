from flask import Blueprint, request, jsonify
from ..models.metodo_pago_model import MetodoPago
from ..schemas.metodo_pago_schema import MetodoPagoSchema
from app import db  # Asegúrate de importar db desde tu archivo de configuración

metodo_pago_bp = Blueprint('metodo_pago_bp', __name__)
metodo_pago_schema = MetodoPagoSchema(session=db.session)
metodos_pago_schema = MetodoPagoSchema(many=True)

# Obtener todos los métodos de pago
@metodo_pago_bp.route('/metodos_pago', methods=['GET'])
def get_metodos_pago():
    try:
        metodos = MetodoPago.query.all()
        return jsonify(metodos_pago_schema.dump(metodos))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un método de pago por ID
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['GET'])
def get_metodo_pago(id):
    try:
        metodo_pago = MetodoPago.query.get_or_404(id)
        return jsonify(metodo_pago_schema.dump(metodo_pago))  # Usamos dump() en lugar de jsonify()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Crear un nuevo método de pago
@metodo_pago_bp.route('/metodos_pago', methods=['POST'])
def add_metodo_pago():
    try:
        data = metodo_pago_schema.load(request.json)  # Cargar los datos del cuerpo de la solicitud
        nuevo_metodo = MetodoPago(**data)  # Crear una nueva instancia de MetodoPago
        db.session.add(nuevo_metodo)
        db.session.commit()
        return jsonify(metodo_pago_schema.dump(nuevo_metodo)), 201  # Devolver el nuevo método creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@metodo_pago_bp.route('/metodos_pago/<string:nombre>', methods=['GET'])
def get_Metodo_pago_por_nombre(nombre):
    try:
        # Búsqueda parcial, no case-sensitive
        metodo_pago = MetodoPago.query.filter(MetodoPago.nombre.ilike(f"%{nombre}%")).all()
        
        if not metodo_pago:
            return jsonify({"error": f"No se encontraron Metodo_pagoes con nombre que contenga '{nombre}'"}), 404
        
        return jsonify(metodos_pago_schema.dump(metodo_pago))
    except Exception as e:
        return jsonify({"error": f"Error al obtener Metodo_pagoes con nombre que contenga '{nombre}': {str(e)}"}), 500


# Actualizar un método de pago existente
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['PUT'])
def update_metodo_pago(id):
    try:
        metodo_pago = MetodoPago.query.get_or_404(id)  # Buscar el método de pago por ID
        data = metodo_pago_schema.load(request.get_json(), partial=True)  # Cargar los nuevos datos
        for key in request.json:
            setattr(metodo_pago, key, getattr(data, key))  # Actualizar los campos del método de pago
        db.session.commit()
        return jsonify(metodo_pago_schema.dump(metodo_pago))  # Devolver el método de pago actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar un método de pago
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['DELETE'])
def delete_metodo_pago(id):
    try:
        metodo_pago = MetodoPago.query.get_or_404(id)  # Buscar el método de pago por ID
        db.session.delete(metodo_pago)  # Eliminar el método de pago
        db.session.commit()
        return jsonify({'message': 'Método de pago eliminado', 'data': metodo_pago_schema.dump(metodo_pago)}), 200  # Devolver el método de pago eliminado
    except Exception as e:
        return jsonify({"error": str(e)}), 500
