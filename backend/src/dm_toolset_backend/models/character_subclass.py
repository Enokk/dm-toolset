from sqlmodel import Field, SQLModel


class CharacterSubclass(SQLModel, table=True):
    __tablename__ = "character_subclass"

    id: int | None = Field(default=None, primary_key=True)
    character_class_id: int = Field(foreign_key="character_class.id")
    name: str
