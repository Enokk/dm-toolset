import enum

from sqlmodel import Field, SQLModel


class ArmorCategory(str, enum.Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SHIELD = "shield"


class Armor(SQLModel, table=True):
    __tablename__ = "armor"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: ArmorCategory
    ac: int
    dex_bonus_applies: bool = Field(default=True)
    dex_bonus_max: int | None = Field(default=None)
    strength_requirement: int | None = Field(default=None)
    stealth_disadvantage: bool = Field(default=False)
    weight_kg: float
    cost_gp: float
