"""empty message

Revision ID: 38370637b05c
Revises: 
Create Date: 2023-03-17 21:20:34.190294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38370637b05c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('sex', sa.String(1), nullable=False),
        sa.Column('address', sa.Text, nullable=False),
        sa.Column('phone', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('pob', sa.String(255), nullable=False),
        sa.Column('dob', sa.Date, nullable=False),
        sa.Column('emergency_contact_name', sa.String(255), nullable=False),
        sa.Column('emergency_contact_phone', sa.String(255), nullable=False),
        sa.Column('emergenct_contact_relationship',
                  sa.String(255), nullable=False),
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
    op.drop_table('patients')
