from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
import cloudinary

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    app.config.from_object(Config)
    
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
    
    cloudinary.config(
        cloud_name = 'TU_CLOUD_NAME',
        api_key = 'TU_API_KEY',
        api_secret = 'TU_API_SECRET',
        secure = True
    )
    
    
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # Importar y registrar los blueprints dentro de la función `create_app` para evitar importación circular
    from .routes.cliente_routes import cliente_bp
    from .routes.producto_routes import producto_bp
    from .routes.venta_routes import venta_bp
    from .routes.categoria_routes import categoria_bp
    from .routes.marca_routes import marca_bp
    from .routes.movimiento_routes import movimiento_bp
    from .routes.rol_routes import rol_bp
    from .routes.permiso_routes import permiso_bp
    from .routes.usuario_routes import usuario_bp
    from .routes.rol_permiso_routes import rol_permiso_bp
    from .routes.auth_routes import auth_bp
    from .routes.bitacora_routes import bitacora_bp
    from .routes.resena_routes import resena_bp
    from .routes.metodo_pago_routes import metodo_pago_bp
    from .routes.cupon_routes import cupon_bp
    from .routes.carrito_routes import carrito_bp
    from .routes.cliente_cupon_routes import cliente_cupon_bp
    from .routes.imagen_producto_routes import imagen_producto_bp

    # Registrar los blueprints
    app.register_blueprint(cliente_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(movimiento_bp)
    app.register_blueprint(rol_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(rol_permiso_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(resena_bp)
    app.register_blueprint(metodo_pago_bp)
    app.register_blueprint(cupon_bp)
    app.register_blueprint(carrito_bp)
    app.register_blueprint(cliente_cupon_bp)
    app.register_blueprint(imagen_producto_bp)

    # print("Rutas registradas:")
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    
    
    
    return app
