from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from dm_toolset_backend.models.character_class import CharacterClass
from dm_toolset_backend.models.character_race import CharacterRace
from dm_toolset_backend.models.character_subclass import CharacterSubclass


class CharacterBase(SQLModel):
    name: str
    level: int
    hit_points_max: int
    hit_points_current: int
    hit_points_temp: int = Field(default=0)
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    copper_pieces: int = Field(default=0)
    silver_pieces: int = Field(default=0)
    gold_pieces: int = Field(default=0)
    platinum_pieces: int = Field(default=0)


class Character(CharacterBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    character_race_id: int = Field(foreign_key="character_race.id")
    character_class_id: int = Field(foreign_key="character_class.id")
    character_subclass_id: int | None = Field(default=None, foreign_key="character_subclass.id")
    character_race: CharacterRace = Relationship()
    character_class: CharacterClass = Relationship()
    character_subclass: CharacterSubclass | None = Relationship()


# Read-only response shape: nests the full CharacterRace/CharacterClass rows (id + name)
# instead of the bare *_id foreign keys, so clients can read
# `character_race.name`/`character_class.name` directly
# without a second round-trip to /character_races or /character_classes.
class CharacterPublic(CharacterBase):
    id: int
    character_race: CharacterRace
    character_class: CharacterClass
    character_subclass: CharacterSubclass | None


class CharacterHitPointsUpdate(SQLModel):
    hit_points_current: int
    hit_points_temp: int


class CharacterCurrencyUpdate(SQLModel):
    copper_pieces: int
    silver_pieces: int
    gold_pieces: int
    platinum_pieces: int
