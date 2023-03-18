"""empty message

Revision ID: 97dfe1ab9c86
Revises: 4277225f5fde
Create Date: 2023-03-18 12:37:12.532577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97dfe1ab9c86'
down_revision = '4277225f5fde'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'consultations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('doctor_id', sa.Integer, nullable=False),
        sa.Column('patient_id', sa.Integer, nullable=False),
        sa.Column('time_slot_id', sa.Integer, nullable=False),
        sa.Column('diagnosis', sa.String(255), nullable=False),
        sa.Column('note', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False,
                  server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=True,
                  onupdate=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint('id'),
        mariadb_collate='utf8mb4_general_ci',
        mariadb_default_charset='utf8mb4',
        mariadb_engine='InnoDB'
    )


def downgrade():
    op.drop_table('doctors')