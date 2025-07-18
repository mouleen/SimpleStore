"""empty message

Revision ID: 795f6860be0a
Revises: 883449008617
Create Date: 2025-07-10 21:07:35.248755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '795f6860be0a'
down_revision = '883449008617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('owner_type', sa.String(length=50), nullable=False))
        batch_op.drop_constraint('images_store_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('images_product_id_fkey', type_='foreignkey')
        batch_op.drop_column('store_id')
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('images_product_id_fkey', 'products', ['product_id'], ['id'])
        batch_op.create_foreign_key('images_store_id_fkey', 'stores', ['store_id'], ['id'])
        batch_op.drop_column('owner_type')
        batch_op.drop_column('owner_id')

    # ### end Alembic commands ###
