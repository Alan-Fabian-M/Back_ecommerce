from app import db

class ImagenProducto(db.Model):
    __tablename__ = 'imagen_producto'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
