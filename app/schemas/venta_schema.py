from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.venta_model import Venta

class VentaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Venta
        load_instance = True
        include_fk = True
        
    metodo_pago_nombre = fields.Method("get_metodo_pago_nombre", dump_only=True)
    cliente_nombre = fields.Method("get_cliente_producto", dump_only=True)
    cupon_nombre = fields.Method("get_cupon_producto", dump_only=True)

    def get_metodo_pago_nombre(self, obj):
        if obj.metodo_pago:
            return obj.metodo_pago.nombre
        return None
    
    def get_cupon_producto(self, obj):
        if obj.cupon:
            return obj.cupon.nombre
        return None
    
    def get_cliente_producto(self, obj):
        if obj.cliente:
            return obj.cliente.nombre
        return None    
    