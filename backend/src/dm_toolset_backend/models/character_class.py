from sqlmodel import Field, SQLModel


class CharacterClass(SQLModel, table=True):
    __tablename__ = "character_class"

    id: int | None = Field(default=None, primary_key=True)
    name: str
