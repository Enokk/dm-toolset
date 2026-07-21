from fastapi import APIRouter, HTTPException
from sqlmodel import select

from dm_toolset_backend.core.db import DBSessionDep
from dm_toolset_backend.models import CharacterClass

router = APIRouter(prefix="/character_classes", tags=["character_classes"])


@router.get("/", response_model=list[CharacterClass])
def get_all_character_classes(session: DBSessionDep) -> list[CharacterClass]:
    return list(session.exec(select(CharacterClass)).all())


@router.get("/{character_class_id}", response_model=CharacterClass)
def get_character_class_by_id(character_class_id: int, session: DBSessionDep) -> CharacterClass:
    character_class = session.get(CharacterClass, character_class_id)
    if character_class is None:
        raise HTTPException(status_code=404, detail="character_class_not_found")
    return character_class
