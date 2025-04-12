from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.cupon_model import Cupon

class CuponSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cupon
        load_instance = True