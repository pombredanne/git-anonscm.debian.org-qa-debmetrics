"""create releases count table

Revision ID: 54556b35c3ff
Revises: 148d137d7335
Create Date: 2014-04-28 11:13:05.426547

"""

# revision identifiers, used by Alembic.
revision = '54556b35c3ff'
down_revision = '148d137d7335'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'releases_count',
            sa.Column('ts', sa.TIMESTAMP, primary_key=True),
            sa.Column('name', sa.Text),
            sa.Column('souce_files', sa.Integer),
            sa.Column('source_packages', sa.Integer),
            sa.Column('disk_usage', sa.Integer),
            sa.Column('ctags', sa.Integer),
            sa.Column('sloc', sa.Integer),
            schema='metrics'
    )


def downgrade():
    op.drop_table(
            'releases_count',
            schema='metrics'
    )
