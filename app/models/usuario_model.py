from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    codigo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    contrasena = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    gmail = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    
    rol = db.relationship('Rol', backref='usuarios')
