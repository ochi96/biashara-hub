"""empty message

Revision ID: 2e00592bb628
Revises: 2958b2875782
Create Date: 2018-12-06 09:48:30.560476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e00592bb628'
down_revision = '2958b2875782'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_reviews_timestamp'), 'reviews', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reviews_timestamp'), table_name='reviews')
    op.drop_column('reviews', 'timestamp')
    # ### end Alembic commands ###
