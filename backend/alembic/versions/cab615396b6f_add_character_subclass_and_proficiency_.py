"""add character subclass and proficiency tables

Revision ID: cab615396b6f
Revises: d8ffd79fc388
Create Date: 2026-08-03 17:02:55.384529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cab615396b6f'
down_revision: Union[str, Sequence[str], None] = 'd8ffd79fc388'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('character_subclass',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_class_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['character_class_id'], ['character_class.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('race_proficiency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_race_id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.Enum('WEAPON', 'ARMOR', name='proficiencykind'), nullable=False),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.Column('weapon_category', sa.Enum('SIMPLE', 'MARTIAL', name='weaponcategory', create_type=False), nullable=True),
    sa.Column('armor_category', sa.Enum('LIGHT', 'MEDIUM', 'HEAVY', 'SHIELD', name='armorcategory', create_type=False), nullable=True),
    sa.ForeignKeyConstraint(['character_race_id'], ['character_race.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['weapon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_proficiency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_class_id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.Enum('WEAPON', 'ARMOR', name='proficiencykind', create_type=False), nullable=False),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.Column('weapon_category', sa.Enum('SIMPLE', 'MARTIAL', name='weaponcategory', create_type=False), nullable=True),
    sa.Column('armor_category', sa.Enum('LIGHT', 'MEDIUM', 'HEAVY', 'SHIELD', name='armorcategory', create_type=False), nullable=True),
    sa.Column('min_level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_class_id'], ['character_class.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['weapon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subclass_proficiency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_subclass_id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.Enum('WEAPON', 'ARMOR', name='proficiencykind', create_type=False), nullable=False),
    sa.Column('weapon_id', sa.Integer(), nullable=True),
    sa.Column('weapon_category', sa.Enum('SIMPLE', 'MARTIAL', name='weaponcategory', create_type=False), nullable=True),
    sa.Column('armor_category', sa.Enum('LIGHT', 'MEDIUM', 'HEAVY', 'SHIELD', name='armorcategory', create_type=False), nullable=True),
    sa.Column('min_level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_subclass_id'], ['character_subclass.id'], ),
    sa.ForeignKeyConstraint(['weapon_id'], ['weapon.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('character', sa.Column('character_subclass_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'character_character_subclass_id_fkey', 'character', 'character_subclass', ['character_subclass_id'], ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('character_character_subclass_id_fkey', 'character', type_='foreignkey')
    op.drop_column('character', 'character_subclass_id')
    op.drop_table('subclass_proficiency')
    op.drop_table('class_proficiency')
    op.drop_table('race_proficiency')
    op.drop_table('character_subclass')
