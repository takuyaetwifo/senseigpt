"""add display_name to User

Revision ID: 4add34d1d88c
Revises: f2e606eb0c9c
Create Date: 2025-05-21 20:32:06.990530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4add34d1d88c'
down_revision = 'f2e606eb0c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('display_name', sa.String(length=80), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('display_name')

    # ### end Alembic commands ###
