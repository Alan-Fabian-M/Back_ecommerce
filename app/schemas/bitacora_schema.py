from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.bitacora_model import Bitacora

class BitacoraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bitacora
        load_instance = True
