from app import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    nit = db.Column(db.String(20))
    gmail = db.Column(db.String(100))
    contrasena = db.Column(db.String(100))
