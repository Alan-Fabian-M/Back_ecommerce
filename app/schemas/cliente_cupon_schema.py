from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.cliente_cupon_model import ClienteCupon

class ClienteCuponSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ClienteCupon
        load_instance = True
        include_fk = True