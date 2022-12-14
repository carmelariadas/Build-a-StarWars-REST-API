"""empty message

Revision ID: 709ad166612a
Revises: f4307a008d5b
Create Date: 2022-11-27 17:42:18.723261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '709ad166612a'
down_revision = 'f4307a008d5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fav__planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fav__planets')
    # ### end Alembic commands ###
