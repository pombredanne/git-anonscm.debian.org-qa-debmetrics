"""create releases table

Revision ID: 148d137d7335
Revises: 41527becd62e
Create Date: 2014-04-28 11:02:45.665761

"""

# revision identifiers, used by Alembic.
revision = '148d137d7335'
down_revision = '41527becd62e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'releases',
            sa.Column('ts', sa.TIMESTAMP, primary_key=True),
            sa.Column('name', sa.Text),
            sa.Column('release_date', sa.Date),
            sa.Column('release_version', sa.Text),
            schema='metrics'
    )


def downgrade():
    op.drop_table(
            'releases',
            schema='metrics'
    )
