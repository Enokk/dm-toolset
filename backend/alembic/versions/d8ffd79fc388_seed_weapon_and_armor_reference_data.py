"""seed weapon and armor reference data

Revision ID: d8ffd79fc388
Revises: 54c781e75f14
Create Date: 2026-08-03 17:02:54.085710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd8ffd79fc388'
down_revision: Union[str, Sequence[str], None] = '54c781e75f14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Full 2014 PHB/SRD weapon and armor tables, transcribed directly from the
# Italian manual (names, weights in kg, costs in gp) rather than derived via a
# lb->kg conversion, and in the same order the manual lists them.

WEAPONS = [
    # name, category, weapon_type, damage_dice, damage_type, properties, versatile_damage_dice, range_normal_m, range_long_m, weight_kg, cost_gp
    # Armi da Mischia Semplici
    ("Ascia", "SIMPLE", "MELEE", "1d6", "TAGLIENTE", ["Leggera", "Lancio"], None, 6, 18, 1, 5),
    ("Bastone Ferrato", "SIMPLE", "MELEE", "1d6", "CONTUNDENTE", ["Versatile"], "1d8", None, None, 2, 0.2),
    ("Falcetto", "SIMPLE", "MELEE", "1d4", "TAGLIENTE", ["Leggera"], None, None, None, 1, 1),
    ("Giavellotto", "SIMPLE", "MELEE", "1d6", "PERFORANTE", ["Lancio"], None, 9, 36, 1, 0.5),
    ("Lancia", "SIMPLE", "MELEE", "1d6", "PERFORANTE", ["Lancio", "Versatile"], "1d8", 6, 18, 1.5, 1),
    ("Martello Leggero", "SIMPLE", "MELEE", "1d4", "CONTUNDENTE", ["Leggera", "Lancio"], None, 6, 18, 1, 2),
    ("Mazza", "SIMPLE", "MELEE", "1d6", "CONTUNDENTE", [], None, None, None, 2, 5),
    ("Pugnale", "SIMPLE", "MELEE", "1d4", "PERFORANTE", ["Accurata", "Leggera", "Lancio"], None, 6, 18, 0.5, 2),
    ("Randello", "SIMPLE", "MELEE", "1d4", "CONTUNDENTE", ["Leggera"], None, None, None, 1, 0.1),
    ("Randello Pesante", "SIMPLE", "MELEE", "1d8", "CONTUNDENTE", ["Due mani"], None, None, None, 5, 0.2),
    # Armi a Distanza Semplici
    ("Arco Corto", "SIMPLE", "RANGED", "1d6", "PERFORANTE", ["Munizioni", "Due mani"], None, 24, 96, 1, 25),
    ("Balestra Leggera", "SIMPLE", "RANGED", "1d8", "PERFORANTE", ["Munizioni", "Ricarica", "Due mani"], None, 24, 96, 2.5, 25),
    ("Dardo", "SIMPLE", "RANGED", "1d4", "PERFORANTE", ["Accurata", "Lancio"], None, 6, 18, 0.125, 0.05),
    ("Fionda", "SIMPLE", "RANGED", "1d4", "CONTUNDENTE", ["Munizioni"], None, 9, 36, 0.0, 0.1),
    # Armi da Mischia da Guerra
    ("Alabarda", "MARTIAL", "MELEE", "1d10", "TAGLIENTE", ["Pesante", "Portata", "Due mani"], None, None, None, 3, 20),
    ("Ascia Bipenne", "MARTIAL", "MELEE", "1d12", "TAGLIENTE", ["Pesante", "Due mani"], None, None, None, 3.5, 30),
    ("Ascia da Battaglia", "MARTIAL", "MELEE", "1d8", "TAGLIENTE", ["Versatile"], "1d10", None, None, 2, 10),
    ("Falcione", "MARTIAL", "MELEE", "1d10", "TAGLIENTE", ["Pesante", "Portata", "Due mani"], None, None, None, 3, 20),
    ("Frusta", "MARTIAL", "MELEE", "1d4", "TAGLIENTE", ["Accurata", "Portata"], None, None, None, 1.5, 2),
    ("Lancia da Cavaliere", "MARTIAL", "MELEE", "1d12", "PERFORANTE", ["Portata", "Speciale"], None, None, None, 3, 10),
    ("Maglio", "MARTIAL", "MELEE", "2d6", "CONTUNDENTE", ["Pesante", "Due mani"], None, None, None, 5, 10),
    ("Martello da Guerra", "MARTIAL", "MELEE", "1d8", "CONTUNDENTE", ["Versatile"], "1d10", None, None, 1, 15),
    ("Mazzafrusto", "MARTIAL", "MELEE", "1d8", "CONTUNDENTE", [], None, None, None, 1, 10),
    ("Morning Star", "MARTIAL", "MELEE", "1d8", "PERFORANTE", [], None, None, None, 2, 15),
    ("Picca", "MARTIAL", "MELEE", "1d10", "PERFORANTE", ["Pesante", "Portata", "Due mani"], None, None, None, 9, 5),
    ("Piccone da Guerra", "MARTIAL", "MELEE", "1d8", "PERFORANTE", [], None, None, None, 1, 5),
    ("Scimitarra", "MARTIAL", "MELEE", "1d6", "TAGLIENTE", ["Accurata", "Leggera"], None, None, None, 1.5, 25),
    ("Spada Corta", "MARTIAL", "MELEE", "1d6", "PERFORANTE", ["Accurata", "Leggera"], None, None, None, 1, 10),
    ("Spada Lunga", "MARTIAL", "MELEE", "1d8", "TAGLIENTE", ["Versatile"], "1d10", None, None, 1.5, 15),
    ("Spadone", "MARTIAL", "MELEE", "2d6", "TAGLIENTE", ["Pesante", "Due mani"], None, None, None, 3, 50),
    ("Stocco", "MARTIAL", "MELEE", "1d8", "PERFORANTE", ["Accurata"], None, None, None, 1, 25),
    ("Tridente", "MARTIAL", "MELEE", "1d6", "PERFORANTE", ["Lancio", "Versatile"], "1d8", 6, 18, 2, 5),
    # Armi a Distanza da Guerra
    ("Arco Lungo", "MARTIAL", "RANGED", "1d8", "PERFORANTE", ["Munizioni", "Pesante", "Due mani"], None, 45, 180, 1, 50),
    ("Balestra a Mano", "MARTIAL", "RANGED", "1d6", "PERFORANTE", ["Munizioni", "Leggera", "Ricarica"], None, 9, 36, 1.5, 75),
    ("Balestra Pesante", "MARTIAL", "RANGED", "1d10", "PERFORANTE", ["Munizioni", "Pesante", "Ricarica", "Due mani"], None, 30, 120, 9, 50),
    ("Cerbottana", "MARTIAL", "RANGED", "1", "PERFORANTE", ["Munizioni", "Ricarica"], None, 7.5, 30, 0.5, 10),
    ("Rete", "MARTIAL", "RANGED", None, None, ["Speciale", "Lancio"], None, 1.5, 4.5, 1.5, 1),
]

ARMORS = [
    # name, category, ac, dex_bonus_applies, dex_bonus_max, strength_requirement, stealth_disadvantage, weight_kg, cost_gp
    ("Imbottita", "LIGHT", 11, True, None, None, True, 4, 5),
    ("Cuoio", "LIGHT", 11, True, None, None, False, 5, 10),
    ("Cuoio Borchiato", "LIGHT", 12, True, None, None, False, 6.5, 45),
    ("Pelle", "MEDIUM", 12, True, 2, None, False, 6, 10),
    ("Giaco di Maglia", "MEDIUM", 13, True, 2, None, False, 10, 50),
    ("Corazza di Scaglie", "MEDIUM", 14, True, 2, None, True, 22.5, 50),
    ("Corazza di Piastre", "MEDIUM", 14, True, 2, None, False, 10, 400),
    ("Mezza Armatura", "MEDIUM", 15, True, 2, None, True, 20, 750),
    ("Corazza ad Anelli", "HEAVY", 14, False, None, None, True, 20, 30),
    ("Cotta di Maglia", "HEAVY", 16, False, None, 13, True, 27.5, 75),
    ("Corazza a Strisce", "HEAVY", 17, False, None, 15, True, 30, 200),
    ("Armatura Completa", "HEAVY", 18, False, None, 15, True, 32.5, 1500),
    ("Scudo", "SHIELD", 2, False, None, None, False, 3, 10),
]

weapon_category_type = sa.Enum("SIMPLE", "MARTIAL", name="weaponcategory", create_type=False)
weapon_type_type = sa.Enum("MELEE", "RANGED", name="weapontype", create_type=False)
damage_type_type = sa.Enum("PERFORANTE", "TAGLIENTE", "CONTUNDENTE", name="damagetype", create_type=False)
armor_category_type = sa.Enum("LIGHT", "MEDIUM", "HEAVY", "SHIELD", name="armorcategory", create_type=False)

weapon_table = sa.table(
    "weapon",
    sa.column("name", sqlmodel.AutoString()),
    sa.column("category", weapon_category_type),
    sa.column("weapon_type", weapon_type_type),
    sa.column("damage_dice", sqlmodel.AutoString()),
    sa.column("damage_type", damage_type_type),
    sa.column("properties", sa.JSON()),
    sa.column("versatile_damage_dice", sqlmodel.AutoString()),
    sa.column("range_normal_m", sa.Float()),
    sa.column("range_long_m", sa.Float()),
    sa.column("weight_kg", sa.Float()),
    sa.column("cost_gp", sa.Float()),
)

armor_table = sa.table(
    "armor",
    sa.column("name", sqlmodel.AutoString()),
    sa.column("category", armor_category_type),
    sa.column("ac", sa.Integer()),
    sa.column("dex_bonus_applies", sa.Boolean()),
    sa.column("dex_bonus_max", sa.Integer()),
    sa.column("strength_requirement", sa.Integer()),
    sa.column("stealth_disadvantage", sa.Boolean()),
    sa.column("weight_kg", sa.Float()),
    sa.column("cost_gp", sa.Float()),
)


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        weapon_table,
        [
            {
                "name": name, "category": category, "weapon_type": weapon_type,
                "damage_dice": damage_dice, "damage_type": damage_type, "properties": properties,
                "versatile_damage_dice": versatile_damage_dice,
                "range_normal_m": range_normal_m, "range_long_m": range_long_m,
                "weight_kg": weight_kg, "cost_gp": cost_gp,
            }
            for name, category, weapon_type, damage_dice, damage_type, properties,
                versatile_damage_dice, range_normal_m, range_long_m, weight_kg, cost_gp in WEAPONS
        ],
    )
    op.bulk_insert(
        armor_table,
        [
            {
                "name": name, "category": category, "ac": ac,
                "dex_bonus_applies": dex_bonus_applies, "dex_bonus_max": dex_bonus_max,
                "strength_requirement": strength_requirement, "stealth_disadvantage": stealth_disadvantage,
                "weight_kg": weight_kg, "cost_gp": cost_gp,
            }
            for name, category, ac, dex_bonus_applies, dex_bonus_max, strength_requirement,
                stealth_disadvantage, weight_kg, cost_gp in ARMORS
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(armor_table.delete())
    op.execute(weapon_table.delete())
