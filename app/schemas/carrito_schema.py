from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.carrito_model import Carrito

class CarritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carrito
        load_instance = True
        include_relationships = True
        include_fk = True
        # Excluimos las relaciones 'venta' y 'producto' del esquema
        cascade='all, delete-orphan'
        passive_deletes=True
        exclude = ('venta', 'producto')

    # Ahora, explícitamente definimos solo los campos que necesitamos
    venta_id = fields.Int(required=True)
    producto_id = fields.Int(required=True)