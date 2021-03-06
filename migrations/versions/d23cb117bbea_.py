"""empty message

Revision ID: d23cb117bbea
Revises: 591cf8d8a7b7
Create Date: 2022-05-11 09:49:43.173944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd23cb117bbea'
down_revision = '591cf8d8a7b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poke_name', sa.String(length=100), nullable=True),
    sa.Column('attack_base_stat', sa.Integer(), nullable=True),
    sa.Column('hp_base_stat', sa.Integer(), nullable=True),
    sa.Column('defense_base_stat', sa.Integer(), nullable=True),
    sa.Column('ability_name', sa.String(length=150), nullable=True),
    sa.Column('base_experience', sa.Integer(), nullable=True),
    sa.Column('front_shiny', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_poke',
    sa.Column('poke_name', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poke_name'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_poke')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
