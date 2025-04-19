from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from ..models.bitacora_model import Bitacora
from ..models.usuario_model import Usuario

class BitacoraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bitacora
        load_instance = True
        
  
    usuario = fields.Method("get_usuario_nombre")

    def get_usuario_nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else None

