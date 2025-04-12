from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.resena_model import Resena

class ResenaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Resena
        load_instance = True