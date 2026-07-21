"""seed class and race reference data

Revision ID: 6ef06728f447
Revises: f26112316832
Create Date: 2026-07-17 19:42:14.178090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

from dm_toolset_backend.models.character_class import ClassName
from dm_toolset_backend.models.character_race import RaceName

# revision identifiers, used by Alembic.
revision: str = '6ef06728f447'
down_revision: Union[str, Sequence[str], None] = 'f26112316832'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Seed rows are derived from the enums (not hardcoded here) so the two stay in
# sync by construction — see the drift note on ClassName/RaceName.
class_table = sa.table("character_class", sa.column("name", sa.Enum(ClassName, name="class_name")))
race_table = sa.table("character_race", sa.column("name", sa.Enum(RaceName, name="race_name")))


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(class_table, [{"name": name} for name in ClassName])
    op.bulk_insert(race_table, [{"name": name} for name in RaceName])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(race_table.delete())
    op.execute(class_table.delete())
