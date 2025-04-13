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

    # Mostrar el nombre en lugar del ID
    categoria = fields.String(attribute="categoria.nombre")
    marca = fields.String(attribute="marca.nombre")

    # Ocultar los campos de ID si no quieres que salgan en el GET (opcional)
    # categoria_id = fields.Int(load_only=True)
    # marca_id = fields.Int(load_only=True)

    # Para POST y PUT con nombre en lugar de ID
    categoria_nombre = fields.String(required=True, load_only=True)
    marca_nombre = fields.String(required=True, load_only=True)

    @validates('categoria_nombre')
    def validar_categoria(self, value):
        categoria = Categoria.query.filter_by(nombre=value).first()
        if not categoria:
            raise ValidationError(f"La categoría '{value}' no existe.")
        self.context['categoria_id'] = categoria.id

    @validates('marca_nombre')
    def validar_marca(self, value):
        marca = Marca.query.filter_by(nombre=value).first()
        if not marca:
            raise ValidationError(f"La marca '{value}' no existe.")
        self.context['marca_id'] = marca.id

    def load(self, data, *args, **kwargs):
        instance = super().load(data, *args, **kwargs)

        # Insertar los IDs en el producto antes de devolverlo
        if 'categoria_id' in self.context:
            instance.categoria_id = self.context['categoria_id']
        if 'marca_id' in self.context:
            instance.marca_id = self.context['marca_id']

        return instance