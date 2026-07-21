from enum import StrEnum

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel


# Source of truth for allowed Class rows: this enum must stay in sync with the
# seed/migration that populates the `class` table (adding/renaming a member here
# without updating the seed causes silent drift).
class ClassName(StrEnum):
    BARBARIAN = "BARBARIAN"
    BARD = "BARD"
    CLERIC = "CLERIC"
    DRUID = "DRUID"
    FIGHTER = "FIGHTER"
    MONK = "MONK"
    PALADIN = "PALADIN"
    RANGER = "RANGER"
    ROGUE = "ROGUE"
    SORCERER = "SORCERER"
    WARLOCK = "WARLOCK"
    WIZARD = "WIZARD"


class CharacterClass(SQLModel, table=True):
    __tablename__ = "character_class"

    id: int | None = Field(default=None, primary_key=True)
    name: ClassName = Field(sa_type=SAEnum(ClassName, name="class_name"))
