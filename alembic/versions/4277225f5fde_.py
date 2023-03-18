"""empty message

Revision ID: 4277225f5fde
Revises: 8fc4dd874503
Create Date: 2023-03-18 10:47:38.117503

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4277225f5fde'
down_revision = '8fc4dd874503'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'doctor_time_slots',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('doctor_id', sa.Integer, nullable=False),
        sa.Column('day', sa.String(255), nullable=False),
        sa.Column('start_time', sa.TIME, nullable=False),
        sa.Column('end_time', sa.TIME, nullable=False),
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
    op.drop_table('doctor_time_slots')
