import os
from contextlib import asynccontextmanager

from sqlalchemy import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.adapter.outgoing.url_model import UrlTableModel
from src.infra.settings import Settings

settings = Settings()

database_url = os.environ.get("DATABASE_URL", settings.DATABASE_URL)
print(f"database url: {database_url}")

# Create an asynchronous engine for the database
engine = create_async_engine(database_url, echo=True, future=True, poolclass=NullPool)


# Asynchronous Context manager for handling database sessions
@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def create_db_and_tables():
    list_of_tables_to_create = [
        UrlTableModel
    ]  # Order Matters when calling SQLModel.metadata.create_all(), you have to import the module that has the models before calling SQLModel.metadata.create_all()
    print(f"creating db tables {list_of_tables_to_create}")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    await engine.dispose()
