from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
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

    # print("Rutas registradas:")
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    
    return app
