from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import (
    InventoryItem,
    InventoryItemPublic,
    InventoryItemCreate,
    InventoryItemUpdate,
)

router = APIRouter(prefix="/characters/{character_id}/inventory", tags=["inventory"])


def _get_item_or_404(character_id: int, item_id: int, session: DBSessionDep) -> InventoryItem:
    item = session.exec(
        select(InventoryItem).where(
            InventoryItem.id == item_id, InventoryItem.character_id == character_id
        )
    ).first()
    if item is None:
        raise HTTPException(status_code=404, detail="inventory_item_not_found")
    return item


@router.get("/", response_model=list[InventoryItemPublic])
def get_inventory(character_id: int, session: DBSessionDep) -> list[InventoryItem]:
    return session.exec(
        select(InventoryItem).where(InventoryItem.character_id == character_id)
    ).all()


@router.post("/", response_model=InventoryItemPublic)
def create_inventory_item(
    character_id: int, payload: InventoryItemCreate, session: DBSessionDep
) -> InventoryItem:
    item = InventoryItem(**payload.model_dump(), character_id=character_id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/{item_id}", response_model=InventoryItemPublic)
def update_inventory_item(
    character_id: int, item_id: int, payload: InventoryItemUpdate, session: DBSessionDep
) -> InventoryItem:
    item = _get_item_or_404(character_id, item_id, session)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def delete_inventory_item(character_id: int, item_id: int, session: DBSessionDep) -> None:
    item = _get_item_or_404(character_id, item_id, session)
    session.delete(item)
    session.commit()
