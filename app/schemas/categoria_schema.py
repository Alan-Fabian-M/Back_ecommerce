
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.categoria_model import Categoria

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        load_instance = True
