from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.venta_model import Venta

class VentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        load_instance = True