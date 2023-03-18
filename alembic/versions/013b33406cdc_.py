"""empty message

Revision ID: 013b33406cdc
Revises: 76213caacb83
Create Date: 2023-03-18 21:57:02.557266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '013b33406cdc'
down_revision = '76213caacb83'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('consultations', 'diagnosis', nullable=True, existing_type=sa.String(255))
    op.alter_column('consultations', 'note', nullable=True, existing_type=sa.TEXT)


def downgrade():
    op.alter_column('consultations', 'note', nullable=False, existing_type=sa.TEXT)
    op.alter_column('consultations', 'diagnosis', nullable=False, existing_type=sa.String(255))
