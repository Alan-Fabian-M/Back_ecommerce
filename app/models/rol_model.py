from app import db

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    
    permisos_relacionados = db.relationship('RolPermiso', backref='rol', cascade='all, delete-orphan')
