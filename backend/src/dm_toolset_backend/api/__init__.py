from fastapi import APIRouter

from dm_toolset_backend.api.characters import router as characters_router
from dm_toolset_backend.api.character_classes import router as character_classes_router
from dm_toolset_backend.api.character_races import router as character_races_router

api_router = APIRouter()
api_router.include_router(characters_router)
api_router.include_router(character_classes_router)
api_router.include_router(character_races_router)
