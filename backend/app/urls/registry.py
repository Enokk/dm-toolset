from ninja import NinjaAPI
from .characters_router import characters_router

# TODO: configura bene NinjaAPI
app_router = NinjaAPI()

app_router.add_router("api/", characters_router)

__all__ = ['app_router']