from app import db

class Cupon(db.Model):
    __tablename__ = 'cupon'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2))
    fecha = db.Column(db.Date)
