from app import db

class ClienteCupon(db.Model):
    __tablename__ = 'cliente_cupon'
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
    cupon_id = db.Column(db.Integer, db.ForeignKey('cupon.id'), primary_key=True)
