"""empty message

Revision ID: 9eb7a9791d32
Revises: 26b969d2a81e
Create Date: 2022-01-20 13:20:22.519183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eb7a9791d32'
down_revision = '26b969d2a81e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed', sa.Column('status', sa.String(length=64), nullable=True))
    op.add_column('cars', sa.Column('transmission', sa.String(length=64), nullable=True))
    op.add_column('cars', sa.Column('seats', sa.Integer(), nullable=True))
    op.add_column('cars', sa.Column('luggage', sa.Integer(), nullable=True))
    op.add_column('cars', sa.Column('fuel', sa.String(length=64), nullable=True))
    op.add_column('cars', sa.Column('engine', sa.String(length=64), nullable=True))
    op.add_column('transactions', sa.Column('status', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transactions', 'status')
    op.drop_column('cars', 'engine')
    op.drop_column('cars', 'fuel')
    op.drop_column('cars', 'luggage')
    op.drop_column('cars', 'seats')
    op.drop_column('cars', 'transmission')
    op.drop_column('borrowed', 'status')
    # ### end Alembic commands ###