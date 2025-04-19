from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates, post_load
from ..models.movimiento_model import Movimiento
from ..models.producto_model import Producto


class MovimientoSchema(SQLAlchemyAutoSchema):
    # producto_nombre = fields.String(required=True, load_only=True)
    # Método para serializar el nombre del producto (esto es opcional)
    producto_nombre = fields.Method("get_producto_nombre")
    usuario_nombre = fields.Method("get_usuario_nombre")

    def get_producto_nombre(self, obj):
        return obj.producto.nombre if obj.producto else None
    def get_usuario_nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else None
    # producto_id = fields.Integer(dump_only=True)  # Para la salida

    class Meta:
        model = Movimiento
        load_instance = True
        include_fk = True
        # exclude = ("producto_id",)

    