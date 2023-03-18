"""empty message

Revision ID: 76213caacb83
Revises: 97dfe1ab9c86
Create Date: 2023-03-18 21:42:56.079349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76213caacb83'
down_revision = '97dfe1ab9c86'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('doctor_time_slots', sa.Column(
        'is_active', sa.BOOLEAN, nullable=False, server_default='1'))


def downgrade():
    op.drop_column('doctor_time_slots', 'is_active')
