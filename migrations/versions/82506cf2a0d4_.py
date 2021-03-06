"""empty message

Revision ID: 82506cf2a0d4
Revises: d23cb117bbea
Create Date: 2022-05-11 15:33:38.777624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82506cf2a0d4'
down_revision = 'd23cb117bbea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_poke_poke_name_fkey', 'user_poke', type_='foreignkey')
    op.create_foreign_key(None, 'user_poke', 'pokemon', ['poke_name'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_poke', type_='foreignkey')
    op.create_foreign_key('user_poke_poke_name_fkey', 'user_poke', 'user', ['poke_name'], ['id'])
    # ### end Alembic commands ###
