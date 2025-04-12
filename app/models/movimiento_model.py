from app import db

class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    id = db.Column(db.Integer, primary_key=True)
    tipomovimiento = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('usuario.codigo'))
