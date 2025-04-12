from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.imagen_producto_model import ImagenProducto

class ImagenProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ImagenProducto
        load_instance = True
        include_fk = True