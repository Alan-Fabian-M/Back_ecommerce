from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.carrito_model import Carrito

class CarritoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Carrito
        load_instance = True