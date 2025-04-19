from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates, post_load
from ..models.resena_model import Resena
from ..models.cliente_model import Cliente
from ..models.producto_model import Producto


class ResenaSchema(SQLAlchemyAutoSchema):
 
    class Meta:
        model = Resena
        load_instance = True
        include_fk = True
        # exclude = ("cliente_id", "producto_id")
        
    producto_nombre = fields.Method("get_nombre_producto", dump_only=True)
    cliente_nombre = fields.Method("get_cliente_producto", dump_only=True)

    def get_nombre_producto(self, obj):
        if obj.producto:
            return obj.producto.nombre
        return None
    
    def get_cliente_producto(self, obj):
        if obj.cliente:
            return obj.cliente.nombre
        return None
