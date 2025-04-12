from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.cliente_model import Cliente

class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True
