"""seed subclasses and weapon armor proficiencies

Revision ID: 61164acc8460
Revises: cab615396b6f
Create Date: 2026-08-03 17:02:57.181658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '61164acc8460'
down_revision: Union[str, Sequence[str], None] = 'cab615396b6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Only weapon/armor proficiencies from the 2014 PHB are modeled here; skill,
# tool, saving-throw and language proficiencies are out of scope for now (see
# docs/character-domain-model.md). Background is not a source in the PHB for
# this subset, so it is intentionally absent.

SUBCLASSES: dict[str, list[str]] = {
    "Barbaro": ["Via del Berserker", "Via del Guerriero Totemico"],
    "Bardo": ["Collegio della Conoscenza", "Collegio del Valore"],
    "Chierico": [
        "Dominio della Conoscenza", "Dominio della Vita", "Dominio della Luce",
        "Dominio della Natura", "Dominio della Tempesta", "Dominio dell'Inganno",
        "Dominio della Guerra",
    ],
    "Druido": ["Circolo della Terra", "Circolo della Luna"],
    "Guerriero": ["Campione", "Maestro di Battaglia", "Cavaliere Mistico"],
    "Ladro": ["Furfante", "Assassino", "Misticatore Arcano"],
    "Mago": [
        "Scuola di Abiurazione", "Scuola di Evocazione", "Scuola di Divinazione",
        "Scuola di Ammaliamento", "Scuola di Invocazione", "Scuola di Illusione",
        "Scuola di Necromanzia", "Scuola di Trasmutazione",
    ],
    "Monaco": ["Via della Mano Aperta", "Via dell'Ombra", "Via dei Quattro Elementi"],
    "Paladino": ["Giuramento di Devozione", "Giuramento degli Antichi", "Giuramento di Vendetta"],
    "Ranger": ["Cacciatore", "Signore delle Bestie"],
    "Stregone": ["Progenie Draconica", "Magia Selvaggia"],
    "Warlock": ["Il Signore Fatato", "L'Immondo", "Il Grande Antico"],
}

# Base class proficiencies (always min_level 1, no choices involved for weapons/armor)
CLASS_ARMOR_CATEGORY: dict[str, list[str]] = {
    "Barbaro": ["LIGHT", "MEDIUM", "SHIELD"],
    "Bardo": ["LIGHT"],
    "Chierico": ["LIGHT", "MEDIUM", "SHIELD"],
    "Druido": ["LIGHT", "MEDIUM", "SHIELD"],
    "Guerriero": ["LIGHT", "MEDIUM", "HEAVY", "SHIELD"],
    "Ladro": ["LIGHT"],
    "Paladino": ["LIGHT", "MEDIUM", "HEAVY", "SHIELD"],
    "Ranger": ["LIGHT", "MEDIUM", "SHIELD"],
    "Warlock": ["LIGHT"],
}

CLASS_WEAPON_CATEGORY: dict[str, list[str]] = {
    "Barbaro": ["SIMPLE", "MARTIAL"],
    "Bardo": ["SIMPLE"],
    "Chierico": ["SIMPLE"],
    "Guerriero": ["SIMPLE", "MARTIAL"],
    "Ladro": ["SIMPLE"],
    "Monaco": ["SIMPLE"],
    "Paladino": ["SIMPLE", "MARTIAL"],
    "Ranger": ["SIMPLE", "MARTIAL"],
    "Warlock": ["SIMPLE"],
}

CLASS_WEAPON_NAMED: dict[str, list[str]] = {
    "Bardo": ["Balestra a mano", "Spada lunga", "Stocco", "Spada corta"],
    "Ladro": ["Balestra a mano", "Spada lunga", "Stocco", "Spada corta"],
    "Monaco": ["Spada corta"],
    "Druido": [
        "Randello", "Pugnale", "Giavellotto", "Mazza", "Bastone ferrato",
        "Scimitarra", "Falcetto", "Fionda", "Lancia",
    ],
    "Mago": ["Pugnale", "Dardo", "Fionda", "Bastone ferrato", "Balestra leggera"],
    "Stregone": ["Pugnale", "Dardo", "Fionda", "Bastone ferrato", "Balestra leggera"],
}

# Race proficiencies: fixed, no choices — only Elfo and Nano grant weapons,
# only Nano delle Montagne grants armor (PHB 2014)
RACE_WEAPON_NAMED: dict[str, list[str]] = {
    "Alto Elfo": ["Spada lunga", "Spada corta", "Arco corto", "Arco lungo"],
    "Elfo dei Boschi": ["Spada lunga", "Spada corta", "Arco corto", "Arco lungo"],
    "Elfo Oscuro (Drow)": ["Spada lunga", "Spada corta", "Arco corto", "Arco lungo"],
    "Nano delle Colline": ["Ascia da Battaglia", "Ascia", "Martello leggero", "Martello da guerra"],
    "Nano delle Montagne": ["Ascia da Battaglia", "Ascia", "Martello leggero", "Martello da guerra"],
}

RACE_ARMOR_CATEGORY: dict[str, list[str]] = {
    "Nano delle Montagne": ["LIGHT", "MEDIUM"],
}

# Subclass bonus proficiencies: only Chierico's Vita/Natura/Tempesta/Guerra
# domains and Bardo's Collegio del Valore grant weapon/armor beyond the base
# class in the 2014 PHB core subclasses; all others grant none.
SUBCLASS_ARMOR_CATEGORY: dict[tuple[str, str], tuple[list[str], int]] = {
    ("Chierico", "Dominio della Vita"): (["HEAVY"], 1),
    ("Chierico", "Dominio della Natura"): (["HEAVY"], 1),
    ("Chierico", "Dominio della Tempesta"): (["HEAVY"], 1),
    ("Chierico", "Dominio della Guerra"): (["HEAVY"], 1),
    ("Bardo", "Collegio del Valore"): (["MEDIUM", "SHIELD"], 3),
}

SUBCLASS_WEAPON_CATEGORY: dict[tuple[str, str], tuple[list[str], int]] = {
    ("Chierico", "Dominio della Tempesta"): (["MARTIAL"], 1),
    ("Chierico", "Dominio della Guerra"): (["MARTIAL"], 1),
    ("Bardo", "Collegio del Valore"): (["MARTIAL"], 3),
}

proficiency_kind_type = sa.Enum("WEAPON", "ARMOR", name="proficiencykind", create_type=False)
weapon_category_type = sa.Enum("SIMPLE", "MARTIAL", name="weaponcategory", create_type=False)
armor_category_type = sa.Enum("LIGHT", "MEDIUM", "HEAVY", "SHIELD", name="armorcategory", create_type=False)

character_class_table = sa.table(
    "character_class", sa.column("id", sa.Integer()), sa.column("name", sqlmodel.AutoString())
)
character_race_table = sa.table(
    "character_race", sa.column("id", sa.Integer()), sa.column("name", sqlmodel.AutoString())
)
weapon_table = sa.table(
    "weapon", sa.column("id", sa.Integer()), sa.column("name", sqlmodel.AutoString())
)
character_subclass_table = sa.table(
    "character_subclass",
    sa.column("id", sa.Integer()),
    sa.column("character_class_id", sa.Integer()),
    sa.column("name", sqlmodel.AutoString()),
)
race_proficiency_table = sa.table(
    "race_proficiency",
    sa.column("character_race_id", sa.Integer()),
    sa.column("kind", proficiency_kind_type),
    sa.column("weapon_id", sa.Integer()),
    sa.column("weapon_category", weapon_category_type),
    sa.column("armor_category", armor_category_type),
)
class_proficiency_table = sa.table(
    "class_proficiency",
    sa.column("character_class_id", sa.Integer()),
    sa.column("kind", proficiency_kind_type),
    sa.column("weapon_id", sa.Integer()),
    sa.column("weapon_category", weapon_category_type),
    sa.column("armor_category", armor_category_type),
    sa.column("min_level", sa.Integer()),
)
subclass_proficiency_table = sa.table(
    "subclass_proficiency",
    sa.column("character_subclass_id", sa.Integer()),
    sa.column("kind", proficiency_kind_type),
    sa.column("weapon_id", sa.Integer()),
    sa.column("weapon_category", weapon_category_type),
    sa.column("armor_category", armor_category_type),
    sa.column("min_level", sa.Integer()),
)


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    class_ids = {
        row.name: row.id
        for row in conn.execute(sa.select(character_class_table.c.id, character_class_table.c.name))
    }
    race_ids = {
        row.name: row.id
        for row in conn.execute(sa.select(character_race_table.c.id, character_race_table.c.name))
    }
    weapon_ids = {
        row.name: row.id
        for row in conn.execute(sa.select(weapon_table.c.id, weapon_table.c.name))
    }

    op.bulk_insert(
        character_subclass_table,
        [
            {"character_class_id": class_ids[class_name], "name": subclass_name}
            for class_name, subclass_names in SUBCLASSES.items()
            for subclass_name in subclass_names
        ],
    )

    subclass_ids = {
        (row.character_class_id, row.name): row.id
        for row in conn.execute(
            sa.select(
                character_subclass_table.c.id,
                character_subclass_table.c.character_class_id,
                character_subclass_table.c.name,
            )
        )
    }

    class_proficiency_rows = []
    for class_name, categories in CLASS_ARMOR_CATEGORY.items():
        for category in categories:
            class_proficiency_rows.append({
                "character_class_id": class_ids[class_name], "kind": "ARMOR",
                "weapon_id": None, "weapon_category": None, "armor_category": category, "min_level": 1,
            })
    for class_name, categories in CLASS_WEAPON_CATEGORY.items():
        for category in categories:
            class_proficiency_rows.append({
                "character_class_id": class_ids[class_name], "kind": "WEAPON",
                "weapon_id": None, "weapon_category": category, "armor_category": None, "min_level": 1,
            })
    for class_name, weapons in CLASS_WEAPON_NAMED.items():
        for weapon_name in weapons:
            class_proficiency_rows.append({
                "character_class_id": class_ids[class_name], "kind": "WEAPON",
                "weapon_id": weapon_ids[weapon_name], "weapon_category": None, "armor_category": None, "min_level": 1,
            })
    op.bulk_insert(class_proficiency_table, class_proficiency_rows)

    race_proficiency_rows = []
    for race_name, weapons in RACE_WEAPON_NAMED.items():
        for weapon_name in weapons:
            race_proficiency_rows.append({
                "character_race_id": race_ids[race_name], "kind": "WEAPON",
                "weapon_id": weapon_ids[weapon_name], "weapon_category": None, "armor_category": None,
            })
    for race_name, categories in RACE_ARMOR_CATEGORY.items():
        for category in categories:
            race_proficiency_rows.append({
                "character_race_id": race_ids[race_name], "kind": "ARMOR",
                "weapon_id": None, "weapon_category": None, "armor_category": category,
            })
    op.bulk_insert(race_proficiency_table, race_proficiency_rows)

    subclass_proficiency_rows = []
    for (class_name, subclass_name), (categories, min_level) in SUBCLASS_ARMOR_CATEGORY.items():
        subclass_id = subclass_ids[(class_ids[class_name], subclass_name)]
        for category in categories:
            subclass_proficiency_rows.append({
                "character_subclass_id": subclass_id, "kind": "ARMOR",
                "weapon_id": None, "weapon_category": None, "armor_category": category, "min_level": min_level,
            })
    for (class_name, subclass_name), (categories, min_level) in SUBCLASS_WEAPON_CATEGORY.items():
        subclass_id = subclass_ids[(class_ids[class_name], subclass_name)]
        for category in categories:
            subclass_proficiency_rows.append({
                "character_subclass_id": subclass_id, "kind": "WEAPON",
                "weapon_id": None, "weapon_category": category, "armor_category": None, "min_level": min_level,
            })
    op.bulk_insert(subclass_proficiency_table, subclass_proficiency_rows)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(subclass_proficiency_table.delete())
    op.execute(class_proficiency_table.delete())
    op.execute(race_proficiency_table.delete())
    op.execute(character_subclass_table.delete())
