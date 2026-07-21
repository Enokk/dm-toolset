from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import CharacterRace

router = APIRouter(prefix="/character_races", tags=["character_races"])


@router.get("/", response_model=list[CharacterRace])
def get_all_character_races(session: DBSessionDep) -> list[CharacterRace]:
    return list(session.exec(select(CharacterRace)).all())


@router.get("/{character_race_id}", response_model=CharacterRace)
def get_character_race_by_id(character_race_id: int, session: DBSessionDep) -> CharacterRace:
    character_race = session.get(CharacterRace, character_race_id)
    if character_race is None:
        raise HTTPException(status_code=404, detail="character_race_not_found")
    return character_race
