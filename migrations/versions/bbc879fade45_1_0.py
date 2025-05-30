"""1.0

Revision ID: bbc879fade45
Revises: 635892f1df76
Create Date: 2025-04-13 15:40:16.859657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc879fade45'
down_revision = '635892f1df76'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.alter_column('telefono',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('telefono',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.alter_column('telefono',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.alter_column('telefono',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)

    # ### end Alembic commands ###
