from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.marca_model import Marca

class MarcaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Marca
        load_instance = True
