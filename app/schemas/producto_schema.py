from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from ..models.producto_model import Producto
from ..models.categoria_model import Categoria
from ..models.marca_model import Marca

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        load_instance = True
        include_fk = True  # Esto sigue siendo útil para POST y PUT


    categoria_nombre = fields.Method("get_categoria_nombre")
    marca_nombre = fields.Method("get_marca_nombre")

    def get_marca_nombre(self, obj):
        return obj.marca.nombre if obj.marca else None
    def get_categoria_nombre(self, obj):
        return obj.categoria.nombre if obj.categoria else None


   