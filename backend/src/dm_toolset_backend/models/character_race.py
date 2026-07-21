from sqlmodel import Field, SQLModel


class CharacterRace(SQLModel, table=True):
    __tablename__ = "character_race"

    id: int | None = Field(default=None, primary_key=True)
    name: str
