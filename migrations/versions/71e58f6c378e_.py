"""empty message

Revision ID: 71e58f6c378e
Revises: 8ac66377cd17
Create Date: 2023-04-14 02:40:32.880954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71e58f6c378e'
down_revision = '8ac66377cd17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article-tag-associations',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article-tag-associations')
    op.drop_table('tags')
    # ### end Alembic commands ###
