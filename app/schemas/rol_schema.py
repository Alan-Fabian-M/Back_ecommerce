from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.rol_model import Rol
from .. import db

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True
        sqla_session = db.session
