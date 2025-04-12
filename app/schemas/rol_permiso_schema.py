from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from ..models.rol_permiso_model import RolPermiso

class RolPermisoSchema(SQLAlchemyAutoSchema):
    rol_id = auto_field(required=True)
    permiso_id = auto_field(required=True)
    
    
    class Meta:
        model = RolPermiso
        load_instance = True
        include_fk = True
