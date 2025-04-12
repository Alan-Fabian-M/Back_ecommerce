from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.metodo_pago_model import MetodoPago

class MetodoPagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MetodoPago
        load_instance = True