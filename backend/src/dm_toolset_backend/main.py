from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dm_toolset_backend.core.config import settings
from dm_toolset_backend.core.db import check_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # `lifespan` e' `async def` per il contratto FastAPI, ma check_connection()
    # e' sincrona e bloccante: qui va bene perche' gira una sola volta all'avvio,
    # prima che il loop debba servire altro.
    check_connection()
    yield


app = FastAPI(title="DM Toolset API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)
