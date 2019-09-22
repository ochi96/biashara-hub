"""empty message

Revision ID: e5c8468e7aa3
Revises: 9c0f0f453c39
Create Date: 2019-09-14 00:09:47.569696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c8468e7aa3'
down_revision = '9c0f0f453c39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_business_businessname', table_name='business')
    op.drop_index('ix_business_id', table_name='business')
    op.drop_index('ix_business_timestamp', table_name='business')
    op.drop_table('business')
    op.drop_index('ix_reviews_id', table_name='reviews')
    op.drop_index('ix_reviews_timestamp', table_name='reviews')
    op.drop_table('reviews')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('feedback', sa.VARCHAR(length=200), nullable=True),
    sa.Column('business_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_reviews_timestamp', 'reviews', ['timestamp'], unique=False)
    op.create_index('ix_reviews_id', 'reviews', ['id'], unique=False)
    op.create_table('business',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('businessname', sa.VARCHAR(length=64), nullable=True),
    sa.Column('about_business', sa.VARCHAR(length=200), nullable=True),
    sa.Column('location', sa.VARCHAR(length=200), nullable=True),
    sa.Column('category', sa.VARCHAR(length=200), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_business_timestamp', 'business', ['timestamp'], unique=False)
    op.create_index('ix_business_id', 'business', ['id'], unique=False)
    op.create_index('ix_business_businessname', 'business', ['businessname'], unique=1)
    # ### end Alembic commands ###
