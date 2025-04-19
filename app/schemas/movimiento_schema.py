from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates, post_load
from ..models.movimiento_model import Movimiento
from ..models.producto_model import Producto


class MovimientoSchema(SQLAlchemyAutoSchema):
    producto_nombre = fields.String(required=True, load_only=True)
    # Método para serializar el nombre del producto (esto es opcional)
    producto = fields.Method("get_producto_nombre")

    def get_producto_nombre(self, obj):
        return obj.producto.nombre if obj.producto else None
    # producto_id = fields.Integer(dump_only=True)  # Para la salida

    class Meta:
        model = Movimiento
        load_instance = True
        include_fk = True
        # exclude = ("producto_id",)

    @validates('producto_nombre')
    def validar_producto(self, value):
        producto = Producto.query.filter_by(nombre=value).first()
        if not producto:
            raise ValidationError(f"El producto '{value}' no existe.")
        # No asignamos self.producto_id aquí

    @post_load
    def asignar_producto_id(self, data, **kwargs):
        nombre_producto = data.pop('producto_nombre')
        producto = Producto.query.filter_by(nombre=nombre_producto).first()
        data['producto_id'] = producto.id
        return data

    usuario = fields.Method("get_usuario_nombre")
    def get_usuario_nombre(self, obj):
        return obj.usuario.nombre if obj.usuario else None

    def make_object(self, data):
        # make_object ahora recibirá 'producto_id' directamente en 'data'
        return super().make_object(data)