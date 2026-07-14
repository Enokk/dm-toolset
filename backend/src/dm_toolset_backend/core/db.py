from collections.abc import Generator

from sqlalchemy import text
from sqlmodel import Session, create_engine

from dm_toolset_backend.core.config import settings

engine = create_engine(settings.database_url)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def check_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
