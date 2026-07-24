"""add speed to character_race

Revision ID: c8d4f2a91e3b
Revises: f3a9c1d8b2e4
Create Date: 2026-07-24 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c8d4f2a91e3b'
down_revision: Union[str, Sequence[str], None] = 'f3a9c1d8b2e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Base walking speed in meters per PHB race.
RACE_SPEEDS = {
    "Alto Elfo": 9,
    "Elfo dei Boschi": 10.5,
    "Elfo Oscuro (Drow)": 9,
    "Halfling Piediveloci": 7.5,
    "Halfling Robusto": 7.5,
    "Nano delle Colline": 7.5,
    "Nano delle Montagne": 7.5,
    "Umano": 9,
    "Umano Variante": 9,
    "Draconide": 9,
    "Gnomo dei Boschi": 7.5,
    "Gnomo delle Rocce": 7.5,
    "Mezzelfo": 9,
    "Mezzorco": 9,
    "Tiefling": 9,
}

race_table = sa.table(
    "character_race",
    sa.column("name", sqlmodel.AutoString()),
    sa.column("speed", sa.Float()),
)


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('character_race', sa.Column('speed', sa.Float(), nullable=False, server_default='9'))
    op.alter_column('character_race', 'speed', server_default=None)

    connection = op.get_bind()
    for name, speed in RACE_SPEEDS.items():
        connection.execute(race_table.update().where(race_table.c.name == name).values(speed=speed))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('character_race', 'speed')
