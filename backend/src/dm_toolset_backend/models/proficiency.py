import enum
from typing import Literal

from sqlmodel import Field, SQLModel

from dm_toolset_backend.models.weapon import WeaponCategory
from dm_toolset_backend.models.armor import ArmorCategory


class ProficiencyKind(str, enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"


ProficiencySource = Literal["race", "class", "subclass"]

# - kind=WEAPON: exactly one of weapon_id (a specific weapon) or weapon_category
#   (a blanket "all simple/martial weapons" grant) is set.
# - kind=ARMOR: armor_category is set; there is no armor_id equivalent, since
#   armor proficiency is always granted by category, never by a named piece.


class ProficiencyBase(SQLModel):
    kind: ProficiencyKind
    weapon_id: int | None = Field(default=None, foreign_key="weapon.id")
    weapon_category: WeaponCategory | None = Field(default=None)
    armor_category: ArmorCategory | None = Field(default=None)


class RaceProficiency(ProficiencyBase, table=True):
    __tablename__ = "race_proficiency"

    id: int | None = Field(default=None, primary_key=True)
    character_race_id: int = Field(foreign_key="character_race.id")


class ClassProficiency(ProficiencyBase, table=True):
    __tablename__ = "class_proficiency"

    id: int | None = Field(default=None, primary_key=True)
    character_class_id: int = Field(foreign_key="character_class.id")
    min_level: int = Field(default=1)


class SubclassProficiency(ProficiencyBase, table=True):
    __tablename__ = "subclass_proficiency"

    id: int | None = Field(default=None, primary_key=True)
    character_subclass_id: int = Field(foreign_key="character_subclass.id")
    min_level: int = Field(default=1)


# Read-only, resolved from RaceProficiency/ClassProficiency/SubclassProficiency —
# never stored against the character, always derived from race + class + subclass + level.
class ProficiencyEntry(SQLModel):
    name: str
    is_category: bool
    source: ProficiencySource


class ProficienciesPublic(SQLModel):
    weapons: list[ProficiencyEntry]
    armor: list[ProficiencyEntry]
