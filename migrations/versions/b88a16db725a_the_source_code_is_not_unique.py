"""the source code is not unique

Revision ID: b88a16db725a
Revises: 0da754909900
Create Date: 2019-01-23 11:54:37.859014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b88a16db725a'
down_revision = '0da754909900'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('source', sa.Column('code', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('source', 'code')
    # ### end Alembic commands ###