"""empty message

Revision ID: 8fc4dd874503
Revises: bbd7a80909f1
Create Date: 2023-03-17 22:30:15.038864

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8fc4dd874503'
down_revision = 'bbd7a80909f1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('license_no', sa.String(255), nullable=False),
        sa.Column('speciality_id', sa.Integer, nullable=False),
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
