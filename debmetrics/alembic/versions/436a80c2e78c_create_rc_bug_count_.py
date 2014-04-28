"""create rc bug count table

Revision ID: 436a80c2e78c
Revises: 54556b35c3ff
Create Date: 2014-04-28 11:18:04.837218

"""

# revision identifiers, used by Alembic.
revision = '436a80c2e78c'
down_revision = '54556b35c3ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
            'rc_bug_count',
            sa.Column('ts', sa.TIMESTAMP, primary_key=True),
            sa.Column('rc_bugs', sa.Integer),
            sa.Column('with_patch', sa.Integer),
            sa.Column('with_fix', sa.Integer),
            sa.Column('ignored', sa.Integer),
            sa.Column('concern_current_stable', sa.Integer),
            sa.Column('concern_next_release', sa.Integer),
            schema='metrics'
    )


def downgrade():
    op.drop_table(
            'rc_bug_count',
            schema='metrics'
    )
