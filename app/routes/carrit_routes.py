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

# Crear un nuevo carrito
@carrito_bp.route('/carritos', methods=['POST'])
def add_carrito():
    try:
        data = carrito_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        nuevo_carrito = Carrito(**data)
        db.session.add(nuevo_carrito)
        db.session.commit()
        return jsonify(carrito_schema.dump(nuevo_carrito)), 201  # Devolver el carrito creado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un carrito existente
@carrito_bp.route('/carritos/<int:id>', methods=['PUT'])
def update_carrito(id):
    try:
        carrito = Carrito.query.get_or_404(id)  # Si no existe, devuelve un error 404
        data = carrito_schema.load(request.json)  # Cargar y validar los datos con Marshmallow
        for key, value in data.items():
            setattr(carrito, key, value)  # Actualizar los atributos del carrito
        db.session.commit()
        return jsonify(carrito_schema.dump(carrito))  # Retornar el carrito actualizado
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un carrito
@carrito_bp.route('/carritos/<int:id>', methods=['DELETE'])
def delete_carrito(id):
    try:
        carrito = Carrito.query.get_or_404(id)
        db.session.delete(carrito)
        db.session.commit()
        return jsonify({'message': 'Carrito eliminado'}), 200  # Respuesta exitosa
    except Exception as e:
        return jsonify({"error": str(e)}), 500
