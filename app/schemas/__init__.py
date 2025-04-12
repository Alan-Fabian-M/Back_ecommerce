
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.categoria_model import Categoria
from app.models.marca_model import Marca
from app.models.usuario_model import Usuario
from app.models.movimiento_model import Movimiento
from app.models.rol_model import Rol
from app.models.permiso_model import Permiso
from app.models.rol_permiso_model import RolPermiso
from app.models.cliente_model import Cliente
from app.models.cupon_model import Cupon
from app.models.cliente_cupon_model import ClienteCupon
from app.models.metodo_pago_model import MetodoPago
from app.models.venta_model import Venta
from app.models.resena_model import Resena
from app.models.producto_model import Producto
from app.models.imagen_producto_model import ImagenProducto
from app.models.carrito_model import Carrito
from app.models.bitacora_model import Bitacora