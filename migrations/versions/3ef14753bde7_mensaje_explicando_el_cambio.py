"""mensaje explicando el cambio

Revision ID: 3ef14753bde7
Revises: 
Create Date: 2025-04-13 15:15:39.266938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef14753bde7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('nit', sa.String(length=20), nullable=True),
    sa.Column('gmail', sa.String(length=100), nullable=True),
    sa.Column('contrasena', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cupon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('monto', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('marca',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metodo_pago',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permiso',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cliente_cupon',
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.Column('cupon_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.ForeignKeyConstraint(['cupon_id'], ['cupon.id'], ),
    sa.PrimaryKeyConstraint('cliente_id', 'cupon_id')
    )
    op.create_table('producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.Column('stock_minimo', sa.Integer(), nullable=True),
    sa.Column('stock_maximo', sa.Integer(), nullable=True),
    sa.Column('precio', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('garantia', sa.Text(), nullable=True),
    sa.Column('categoria_id', sa.Integer(), nullable=True),
    sa.Column('marca_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], ),
    sa.ForeignKeyConstraint(['marca_id'], ['marca.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rol_permiso',
    sa.Column('rol_id', sa.Integer(), nullable=False),
    sa.Column('permiso_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permiso_id'], ['permiso.id'], ),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], ),
    sa.PrimaryKeyConstraint('rol_id', 'permiso_id')
    )
    op.create_table('usuario',
    sa.Column('codigo', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('apellido', sa.String(length=100), nullable=True),
    sa.Column('contrasena', sa.String(length=255), nullable=True),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('gmail', sa.String(length=100), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('rol_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rol_id'], ['rol.id'], ),
    sa.PrimaryKeyConstraint('codigo')
    )
    op.create_table('venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('importe_total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('importe_total_desc', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.Column('metodo_pago_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.ForeignKeyConstraint(['metodo_pago_id'], ['metodo_pago.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bitacora',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('accion', sa.Text(), nullable=True),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('hora', sa.Time(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('usuario_codigo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_codigo'], ['usuario.codigo'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carrito',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.Column('estado', sa.String(length=50), nullable=True),
    sa.Column('importe', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('importe_desc', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('precio', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('venta_id', sa.Integer(), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.ForeignKeyConstraint(['venta_id'], ['venta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('imagen_producto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movimiento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipomovimiento', sa.String(length=50), nullable=True),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.Column('fecha', sa.Date(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.Column('usuario_codigo', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.ForeignKeyConstraint(['usuario_codigo'], ['usuario.codigo'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resena',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('puntuacion', sa.Integer(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=True),
    sa.Column('producto_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.ForeignKeyConstraint(['producto_id'], ['producto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resena')
    op.drop_table('movimiento')
    op.drop_table('imagen_producto')
    op.drop_table('carrito')
    op.drop_table('bitacora')
    op.drop_table('venta')
    op.drop_table('usuario')
    op.drop_table('rol_permiso')
    op.drop_table('producto')
    op.drop_table('cliente_cupon')
    op.drop_table('rol')
    op.drop_table('permiso')
    op.drop_table('metodo_pago')
    op.drop_table('marca')
    op.drop_table('cupon')
    op.drop_table('cliente')
    op.drop_table('categoria')
    # ### end Alembic commands ###
