from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from dm_toolset_backend.models.character_class import CharacterClass
from dm_toolset_backend.models.character_race import CharacterRace


class CharacterBase(SQLModel):
    name: str
    level: int


class Character(CharacterBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    character_race_id: int = Field(foreign_key="character_race.id")
    character_class_id: int = Field(foreign_key="character_class.id")
    character_race: CharacterRace = Relationship()
    character_class: CharacterClass = Relationship()


# Read-only response shape: nests the full CharacterRace/CharacterClass rows (id + name)
# instead of the bare *_id foreign keys, so clients can localize
# `character_race.name`/`character_class.name` (the RaceName/ClassName enum codes)
# without a second round-trip to /character_races or /character_classes.
class CharacterPublic(CharacterBase):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    character_race: CharacterRace
    character_class: CharacterClass
