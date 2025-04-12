from app import db


class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    importe = db.Column(db.Numeric(10, 2))
    importe_desc = db.Column(db.Numeric(10, 2))
    precio = db.Column(db.Numeric(10, 2))
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
