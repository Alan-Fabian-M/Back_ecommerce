
from app import db

class Bitacora(db.Model):
    __tablename__ = 'bitacora'
    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.Text)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    descripcion = db.Column(db.Text)
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('usuario.codigo'))
