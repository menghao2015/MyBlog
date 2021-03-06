"""C_10_3-8_avatar

Revision ID: c7fed8637228
Revises: 70f548ed4086
Create Date: 2016-03-08 15:27:25.332265

"""

# revision identifiers, used by Alembic.
revision = 'c7fed8637228'
down_revision = '70f548ed4086'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=64), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'avatar_hash')
    ### end Alembic commands ###
