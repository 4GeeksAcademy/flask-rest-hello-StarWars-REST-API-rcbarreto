"""empty message

Revision ID: 459b27ac12e9
Revises: 78c3f321f58f
Create Date: 2024-12-02 00:30:08.064700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459b27ac12e9'
down_revision = '78c3f321f58f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=False))

    # ### end Alembic commands ###