from app import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    stock_minimo = db.Column(db.Integer)
    stock_maximo = db.Column(db.Integer)
    precio = db.Column(db.Numeric(10, 2))
    descripcion = db.Column(db.Text)
    garantia = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'))
