"""add hit points to character

Revision ID: 86ee68e87180
Revises: 7b185c4529a4
Create Date: 2026-07-21 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '86ee68e87180'
down_revision: Union[str, Sequence[str], None] = '7b185c4529a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('character', sa.Column('hit_points_max', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('character', sa.Column('hit_points_current', sa.Integer(), nullable=False, server_default='10'))
    op.add_column('character', sa.Column('hit_points_temp', sa.Integer(), nullable=False, server_default='0'))
    op.alter_column('character', 'hit_points_max', server_default=None)
    op.alter_column('character', 'hit_points_current', server_default=None)
    op.alter_column('character', 'hit_points_temp', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('character', 'hit_points_temp')
    op.drop_column('character', 'hit_points_current')
    op.drop_column('character', 'hit_points_max')
