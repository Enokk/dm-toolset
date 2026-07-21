from enum import StrEnum

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel


# Source of truth for allowed CharacterRace rows: this enum must stay in sync with the
# seed/migration that populates the `character_race` table (adding/renaming a member here
# without updating the seed causes silent drift).
class RaceName(StrEnum):
    DRAGONBORN = "DRAGONBORN"
    DWARF_HILL = "DWARF_HILL"
    DWARF_MOUNTAIN = "DWARF_MOUNTAIN"
    ELF_HIGH = "ELF_HIGH"
    ELF_WOOD = "ELF_WOOD"
    ELF_DARK = "ELF_DARK"
    GNOME_FOREST = "GNOME_FOREST"
    GNOME_ROCK = "GNOME_ROCK"
    HALF_ELF = "HALF_ELF"
    HALF_ORC = "HALF_ORC"
    HALFLING_LIGHTFOOT = "HALFLING_LIGHTFOOT"
    HALFLING_STOUT = "HALFLING_STOUT"
    HUMAN_STANDARD = "HUMAN_STANDARD"
    HUMAN_VARIANT = "HUMAN_VARIANT"
    TIEFLING = "TIEFLING"


class CharacterRace(SQLModel, table=True):
    __tablename__ = "character_race"

    id: int | None = Field(default=None, primary_key=True)
    name: RaceName = Field(sa_type=SAEnum(RaceName, name="race_name"))
