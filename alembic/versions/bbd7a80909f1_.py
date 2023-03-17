"""empty message

Revision ID: bbd7a80909f1
Revises: 38370637b05c
Create Date: 2023-03-17 22:13:19.977277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bbd7a80909f1'
down_revision = '38370637b05c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'specialities',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
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
    op.drop_table('specialities')
