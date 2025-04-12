from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.movimiento_model import Movimiento

class MovimientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movimiento
        load_instance = True
        include_fk = True
