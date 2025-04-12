from app import db

class RolPermiso(db.Model):
    __tablename__ = 'rol_permiso'
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), primary_key=True)
    permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.id'), primary_key=True)
