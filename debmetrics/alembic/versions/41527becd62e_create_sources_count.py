"""create sources count table

Revision ID: 41527becd62e
Revises: None
Create Date: 2014-04-28 10:29:20.237730

"""

# revision identifiers, used by Alembic.
revision = '41527becd62e'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'sources_count',
            sa.Column('ts', sa.TIMESTAMP, primary_key=True),
            sa.Column('arch', sa.Integer),
            sa.Column('bzr', sa.Integer),
            sa.Column('cvs', sa.Integer),
            sa.Column('darcs', sa.Integer),
            sa.Column('git', sa.Integer),
            sa.Column('hg', sa.Integer),
            sa.Column('mtn', sa.Integer),
            sa.Column('svn', sa.Integer),
            sa.Column('total', sa.Integer),
            sa.Column('using_vcs', sa.Integer),
            schema='metrics'
    )


def downgrade():
    op.drop_table(
            'sources_count',
            schema='metrics'
    )
