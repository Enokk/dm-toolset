from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel
from pydantic import field_validator


class InventoryItemBase(SQLModel):
    name: str
    type: str
    subtitle: str | None = None
    quantity: int = Field(default=1)
    is_equippable: bool = Field(default=False)
    is_equipped: bool = Field(default=False)
    equip_slot: str | None = None
    properties: dict = Field(default_factory=dict, sa_column=Column(JSON, nullable=False))


class InventoryItem(InventoryItemBase, table=True):
    __tablename__ = "inventory_item"

    id: int | None = Field(default=None, primary_key=True)
    character_id: int = Field(foreign_key="character.id")


class InventoryItemPublic(InventoryItemBase):
    id: int


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(SQLModel):
    name: str | None = None
    type: str | None = None
    subtitle: str | None = None
    quantity: int | None = None
    is_equippable: bool | None = None
    is_equipped: bool | None = None
    equip_slot: str | None = None
    properties: dict | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        stripped = value.strip()
        if not stripped:
            raise ValueError("name must not be blank")
        return stripped
