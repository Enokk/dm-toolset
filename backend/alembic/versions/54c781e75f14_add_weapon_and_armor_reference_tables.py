"""add weapon and armor reference tables

Revision ID: 54c781e75f14
Revises: f12a04ae8917
Create Date: 2026-08-03 17:02:52.877624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '54c781e75f14'
down_revision: Union[str, Sequence[str], None] = 'f12a04ae8917'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('armor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.AutoString(), nullable=False),
    sa.Column('category', sa.Enum('LIGHT', 'MEDIUM', 'HEAVY', 'SHIELD', name='armorcategory'), nullable=False),
    sa.Column('ac', sa.Integer(), nullable=False),
    sa.Column('dex_bonus_applies', sa.Boolean(), nullable=False),
    sa.Column('dex_bonus_max', sa.Integer(), nullable=True),
    sa.Column('strength_requirement', sa.Integer(), nullable=True),
    sa.Column('stealth_disadvantage', sa.Boolean(), nullable=False),
    sa.Column('weight_kg', sa.Float(), nullable=False),
    sa.Column('cost_gp', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.AutoString(), nullable=False),
    sa.Column('category', sa.Enum('SIMPLE', 'MARTIAL', name='weaponcategory'), nullable=False),
    sa.Column('weapon_type', sa.Enum('MELEE', 'RANGED', name='weapontype'), nullable=False),
    sa.Column('damage_dice', sqlmodel.AutoString(), nullable=True),
    sa.Column('damage_type', sa.Enum('PERFORANTE', 'TAGLIENTE', 'CONTUNDENTE', name='damagetype'), nullable=True),
    sa.Column('properties', sa.JSON(), nullable=False),
    sa.Column('versatile_damage_dice', sqlmodel.AutoString(), nullable=True),
    sa.Column('range_normal_m', sa.Float(), nullable=True),
    sa.Column('range_long_m', sa.Float(), nullable=True),
    sa.Column('weight_kg', sa.Float(), nullable=False),
    sa.Column('cost_gp', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('weapon')
    op.drop_table('armor')
