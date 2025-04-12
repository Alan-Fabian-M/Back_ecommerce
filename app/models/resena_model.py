from app import db

class Resena(db.Model):
    __tablename__ = 'resena'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
