"""add ability scores to character

Revision ID: f3a9c1d8b2e4
Revises: 86ee68e87180
Create Date: 2026-07-22 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f3a9c1d8b2e4'
down_revision: Union[str, Sequence[str], None] = '86ee68e87180'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ABILITY_SCORES = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']


def upgrade() -> None:
    """Upgrade schema."""
    for ability in ABILITY_SCORES:
        op.add_column('character', sa.Column(ability, sa.Integer(), nullable=False, server_default='10'))
    for ability in ABILITY_SCORES:
        op.alter_column('character', ability, server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    for ability in reversed(ABILITY_SCORES):
        op.drop_column('character', ability)
