from app import db

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    importe_total = db.Column(db.Numeric(10, 2))
    importe_total_desc = db.Column(db.Numeric(10, 2))
    estado = db.Column(db.String(50))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'))
    cupon_id = db.Column(db.Integer, db.ForeignKey('cupon.id'))
    
    cliente = db.relationship("Cliente", backref='ventas')
    cupon = db.relationship("Cupon", backref='ventas')
    metodo_pago = db.relationship("MetodoPago", backref='ventas')
    carritos = db.relationship('Carrito', back_populates='venta',cascade='all, delete-orphan',passive_deletes=True)
    