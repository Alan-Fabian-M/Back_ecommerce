from faker import Faker
from datetime import datetime, time
import random
from decimal import Decimal
from werkzeug.security import generate_password_hash


from app import create_app, db
from app.models.cliente_model import Cliente
from app.models.usuario_model import Usuario
from app.models.rol_model import Rol
from app.models.permiso_model import Permiso
from app.models.rol_permiso_model import RolPermiso
from app.models.categoria_model import Categoria
from app.models.marca_model import Marca
from app.models.producto_model import Producto
from app.models.imagen_producto_model import ImagenProducto
from app.models.metodo_pago_model import MetodoPago
from app.models.venta_model import Venta
from app.models.carrito_model import Carrito
from app.models.resena_model import Resena
from app.models.movimiento_model import Movimiento
from app.models.bitacora_model import Bitacora
from app.models.cliente_cupon_model import ClienteCupon
from app.models.cupon_model import Cupon

faker = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        # db.drop_all()
        db.create_all()

        # Roles y Permisos
        rol_admin = Rol(nombre="Admin", descripcion="Administrador")
        rol_cliente = Rol(nombre="Cliente", descripcion="Cliente")
        db.session.add_all([rol_admin, rol_cliente])
        db.session.commit()

        permisos = []
        for nombre in ["crear", "leer", "actualizar", "eliminar"]:
            permiso = Permiso(nombre=nombre, descripcion=f"Permiso para {nombre}")
            db.session.add(permiso)
            db.session.flush()
            permisos.append(permiso)
            db.session.add(RolPermiso(rol_id=rol_admin.id, permiso_id=permiso.id))

        # Usuarios
        usuarios = []
        for _ in range(3):
            user = Usuario(
                nombre=faker.first_name(),
                apellido=faker.last_name(),
                telefono=faker.phone_number(),
                gmail=faker.email(),
                contrasena=generate_password_hash("admin123"),
                estado="activo",
                rol_id=rol_admin.id
            )
            db.session.add(user)
            usuarios.append(user)

        # Clientes
        clientes = []
        for _ in range(10):
            cliente = Cliente(
                nombre=faker.name(),
                telefono=faker.phone_number(),
                nit=str(faker.random_number(digits=8)),
                gmail=faker.email(),
                contrasena=generate_password_hash("cliente123")
            )
            db.session.add(cliente)
            clientes.append(cliente)

        # Categorías y Marcas
        categorias = [Categoria(nombre=faker.word()) for _ in range(5)]
        marcas = [Marca(nombre=faker.company()) for _ in range(5)]
        db.session.add_all(categorias + marcas)
        db.session.commit()

        # Productos e Imágenes
        productos = []
        for _ in range(15):
            producto = Producto(
                nombre=faker.word(),
                stock=random.randint(10, 100),
                stock_minimo=5,
                stock_maximo=150,
                precio=round(random.uniform(10, 500), 2),
                descripcion=faker.sentence(),
                garantia="6 meses",
                categoria_id=random.choice(categorias).id,
                marca_id=random.choice(marcas).id
            )
            db.session.add(producto)
            db.session.flush()
            productos.append(producto)
            db.session.add(ImagenProducto(image_url=faker.image_url(), producto_id=producto.id))

        # Métodos de pago
        pagos = [
            MetodoPago(nombre="Efectivo", descripcion="Pago en efectivo"),
            MetodoPago(nombre="Tarjeta", descripcion="Pago con tarjeta")
        ]
        db.session.add_all(pagos)

        # Cupones y relación Cliente-Cupon
        cupones = []
        for _ in range(5):
            cupon = Cupon(
                nombre=faker.word(),
                descripcion=faker.text(),
                monto=round(random.uniform(5, 50), 2),
                fecha=faker.date_this_year()
            )
            db.session.add(cupon)
            cupones.append(cupon)

        db.session.commit()

        for cliente in clientes:
            cupon = random.choice(cupones)
            db.session.add(ClienteCupon(cliente_id=cliente.id, cupon_id=cupon.id))

        # Ventas, Carritos y Reseñas
        for _ in range(10):
            venta = Venta(
                fecha=datetime.now().date(),
                importe_total=round(random.uniform(100, 1000), 2),
                importe_total_desc=round(random.uniform(80, 950), 2),
                estado="completado",
                cliente_id=random.choice(clientes).id,
                metodo_pago_id=random.choice(pagos).id
            )
            db.session.add(venta)
            db.session.flush()

            for _ in range(2):
                producto = random.choice(productos)
                db.session.add(Carrito(
                    cantidad=random.randint(1, 5),
                    estado="vendido",
                    importe = round(producto.precio * Decimal('1.1'), 2),
                    importe_desc=round(producto.precio, 2),
                    precio=producto.precio,
                    venta_id=venta.id,
                    producto_id=producto.id
                ))
                db.session.add(Resena(
                    descripcion=faker.text(),
                    puntuacion=random.randint(1, 5),
                    cliente_id=venta.cliente_id,
                    producto_id=producto.id
                ))

        # Movimientos y Bitácora
        for _ in range(10):
            db.session.add(Movimiento(
                tipomovimiento=random.choice(["entrada", "salida"]),
                cantidad=random.randint(1, 20),
                fecha=faker.date_this_year(),
                descripcion=faker.text(),
                producto_id=random.choice(productos).id,
                usuario_codigo=random.choice(usuarios).codigo
            ))

            db.session.add(Bitacora(
                accion=faker.word(),
                fecha=faker.date_this_year(),
                hora=time(hour=random.randint(0, 23), minute=random.randint(0, 59)),
                descripcion=faker.text(),
                usuario_codigo=random.choice(usuarios).codigo
            ))

        db.session.commit()
        print("¡Base de datos poblada con datos de prueba exitosamente!")

if __name__ == "__main__":
    seed_data()
