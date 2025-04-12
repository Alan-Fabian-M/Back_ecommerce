from app import db

class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
