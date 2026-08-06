from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import Armor

router = APIRouter(prefix="/armors", tags=["armors"])


@router.get("/", response_model=list[Armor])
def get_all_armors(session: DBSessionDep) -> list[Armor]:
    return list(session.exec(select(Armor)).all())


@router.get("/{armor_id}", response_model=Armor)
def get_armor_by_id(armor_id: int, session: DBSessionDep) -> Armor:
    armor = session.get(Armor, armor_id)
    if armor is None:
        raise HTTPException(status_code=404, detail="armor_not_found")
    return armor
