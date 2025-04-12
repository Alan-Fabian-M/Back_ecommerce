from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.permiso_model import Permiso

class PermisoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permiso
        load_instance = True
        include_fk = True  # solo si hay claves foráneas
