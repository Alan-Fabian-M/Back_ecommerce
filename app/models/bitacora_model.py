from app import db
from ..models.usuario_model import Usuario

class Bitacora(db.Model):
    __tablename__ = 'bitacora'
    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.Text)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    descripcion = db.Column(db.Text)
    ip = db.Column(db.Text)
    usuario_codigo = db.Column(db.Integer, db.ForeignKey('usuario.codigo'))
    
    # Define la relación con el modelo Usuario
    usuario = db.relationship('Usuario', backref='bitacoras')
