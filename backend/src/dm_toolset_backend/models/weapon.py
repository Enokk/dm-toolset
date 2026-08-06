import enum

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class WeaponCategory(str, enum.Enum):
    SIMPLE = "simple"
    MARTIAL = "martial"


class WeaponType(str, enum.Enum):
    MELEE = "melee"
    RANGED = "ranged"


class DamageType(str, enum.Enum):
    PERFORANTE = "perforante"
    TAGLIENTE = "tagliente"
    CONTUNDENTE = "contundente"


class Weapon(SQLModel, table=True):
    __tablename__ = "weapon"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: WeaponCategory
    weapon_type: WeaponType
    # Null for weapons with no standard damage die (e.g. Rete/net, which is Speciale-only)
    damage_dice: str | None = Field(default=None)
    damage_type: DamageType | None = Field(default=None)
    # Plain flag tags only (e.g. "Leggera", "Versatile", "Lancio") — the numeric
    # payload for Versatile/Lancio/Munizioni lives in the dedicated fields below
    # instead of being embedded in the string, so it doesn't need parsing to use.
    properties: list[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    # Set only when "Versatile" is in properties (alternate two-handed damage die)
    versatile_damage_dice: str | None = Field(default=None)
    # Set only when "Lancio" or "Munizioni" is in properties (the two never coexist)
    range_normal_m: float | None = Field(default=None)
    range_long_m: float | None = Field(default=None)
    weight_kg: float
    cost_gp: float
