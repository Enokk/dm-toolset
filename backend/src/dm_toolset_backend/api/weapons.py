from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import Weapon

router = APIRouter(prefix="/weapons", tags=["weapons"])


@router.get("/", response_model=list[Weapon])
def get_all_weapons(session: DBSessionDep) -> list[Weapon]:
    return list(session.exec(select(Weapon)).all())


@router.get("/{weapon_id}", response_model=Weapon)
def get_weapon_by_id(weapon_id: int, session: DBSessionDep) -> Weapon:
    weapon = session.get(Weapon, weapon_id)
    if weapon is None:
        raise HTTPException(status_code=404, detail="weapon_not_found")
    return weapon
