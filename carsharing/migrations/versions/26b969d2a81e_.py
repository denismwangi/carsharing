"""empty message

Revision ID: 26b969d2a81e
Revises: 
Create Date: 2022-01-15 16:33:32.964259

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '26b969d2a81e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('carid', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['carid'], ['cars.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('borrowed', sa.Column('carid', sa.Integer(), nullable=True))
    op.drop_column('borrowed', 'vehicleid')
    op.add_column('cars', sa.Column('borrowed', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'cars', ['regno'])
    op.create_foreign_key(None, 'cars', 'users', ['ownerid'], ['id'])
    op.add_column('transactions', sa.Column('carid', sa.Integer(), nullable=True))
    op.add_column('transactions', sa.Column('amount', sa.Integer(), nullable=True))
    op.drop_column('transactions', 'amountpaid')
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(length=8), nullable=True))
    op.drop_column('users', 'passphrase')
    op.drop_column('users', 'location')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('location', mysql.VARCHAR(length=20), nullable=True))
    op.add_column('users', sa.Column('passphrase', mysql.VARCHAR(length=128), nullable=True))
    op.drop_column('users', 'role')
    op.drop_column('users', 'password_hash')
    op.add_column('transactions', sa.Column('amountpaid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('transactions', 'amount')
    op.drop_column('transactions', 'carid')
    op.drop_constraint(None, 'cars', type_='foreignkey')
    op.drop_constraint(None, 'cars', type_='unique')
    op.drop_column('cars', 'borrowed')
    op.add_column('borrowed', sa.Column('vehicleid', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('borrowed', 'carid')
    op.drop_table('images')
    # ### end Alembic commands ###
