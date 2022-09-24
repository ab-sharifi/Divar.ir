"""First init MIgrate in divar project

Revision ID: b747170fee3b
Revises: 
Create Date: 2022-09-24 11:34:41.354225

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b747170fee3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Histories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('last_visit', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('histories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('histories',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('post_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('last_visit', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Histories')
    # ### end Alembic commands ###
