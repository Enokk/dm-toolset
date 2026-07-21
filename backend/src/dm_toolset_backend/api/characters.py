from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import Character, CharacterPublic

router = APIRouter(prefix="/characters", tags=["characters"])

# selectinload avoids the N+1 that plain Relationship() lazy-loading would cause
# when serializing character_race/character_class for every character in the list endpoint.
_character_select = select(Character).options(
    selectinload(Character.character_race), selectinload(Character.character_class)
)


@router.get("/", response_model=list[CharacterPublic])
def get_all_characters(session: DBSessionDep) -> list[CharacterPublic]:
    characters = session.exec(_character_select).all()
    return [CharacterPublic.model_validate(character) for character in characters]


@router.get("/{character_id}", response_model=CharacterPublic)
def get_character_by_id(character_id: int, session: DBSessionDep) -> CharacterPublic:
    character = session.exec(_character_select.where(Character.id == character_id)).first()
    if character is None:
        raise HTTPException(status_code=404, detail="character_not_found")
    return CharacterPublic.model_validate(character)
