"""init

Revision ID: 7febc574e4c1
Revises: 
Create Date: 2021-07-20 21:51:33.805811

"""
import datetime
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7febc574e4c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'brews',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('created_date', sa.DateTime, nullable=False, default=datetime.datetime.utcnow()),
        sa.Column('startOrStop', sa.Boolean, nullable=False, default=True)
    )


def downgrade():
    op.drop_table('brews')
