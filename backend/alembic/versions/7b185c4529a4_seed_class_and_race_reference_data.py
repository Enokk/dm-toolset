"""seed class and race reference data

Revision ID: 7b185c4529a4
Revises: 2afe0a753770
Create Date: 2026-07-21 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7b185c4529a4'
down_revision: Union[str, Sequence[str], None] = '2afe0a753770'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Initial seed covering the base classes and races from the
# 5e Player's Handbook (PHB).
CLASS_NAMES = [
    "Barbaro",
    "Bardo",
    "Chierico",
    "Druido",
    "Guerriero",
    "Ladro",
    "Mago",
    "Monaco",
    "Paladino",
    "Ranger",
    "Stregone",
    "Warlock",
]

RACE_NAMES = [
    "Alto Elfo",
    "Elfo dei Boschi",
    "Elfo Oscuro (Drow)",
    "Halfling Piediveloci",
    "Halfling Robusto",
    "Nano delle Colline",
    "Nano delle Montagne",
    "Umano",
    "Umano Variante",
    "Draconide",
    "Gnomo dei Boschi",
    "Gnomo delle Rocce",
    "Mezzelfo",
    "Mezzorco",
    "Tiefling",
]

class_table = sa.table("character_class", sa.column("name", sqlmodel.AutoString()))
race_table = sa.table("character_race", sa.column("name", sqlmodel.AutoString()))


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(class_table, [{"name": name} for name in CLASS_NAMES])
    op.bulk_insert(race_table, [{"name": name} for name in RACE_NAMES])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(race_table.delete())
    op.execute(class_table.delete())
