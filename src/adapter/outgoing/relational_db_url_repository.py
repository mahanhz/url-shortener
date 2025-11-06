from typing import Dict

from sqlmodel import select

from src.adapter.outgoing.url_model import UrlTableModel
from src.application.port.outgoing.url_repository import UrlRepository
from src.adapter.outgoing.database import get_session


class RelationalDbUrlRepository(UrlRepository):
    async def list(self) -> Dict[str, str]:
        async with get_session() as session:
            query = select(UrlTableModel)
            result = await session.execute(query)
            return {x.short_url_code: x.original_url for x in result.scalars().all()}

    async def get(self, short_code: str) -> str:
        async with get_session() as session:
            """Get a single record by short code."""
            query = select(UrlTableModel).where(
                UrlTableModel.short_url_code == short_code
            )
            result = await session.execute(query)
            return result.scalars().first().original_url

    async def create(self, payload: dict) -> str:
        async with get_session() as session:
            """Create a new record."""
            url_table_model = UrlTableModel(
                short_url_code=payload["short_url_code"],
                original_url=payload["original_url"],
                created_by=payload["created_by"],
            )
            session.add(url_table_model)
            await session.commit()
            await session.refresh(url_table_model)
            return url_table_model.short_url_code
