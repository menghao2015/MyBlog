"""8_1

Revision ID: daf5f84ca180
Revises: None
Create Date: 2016-01-06 15:50:34.620157

"""

# revision identifiers, used by Alembic.
revision = 'daf5f84ca180'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'password_hash')
    ### end Alembic commands ###
