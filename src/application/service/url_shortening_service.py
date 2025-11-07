from typing import Dict

from src.application.port.incoming.ShorteningService import ShorteningService
from src.application.port.outgoing.short_code_repository import ShortCodeRepository
from src.application.port.outgoing.url_repository import UrlRepository


class UrlShorteningService(ShorteningService):
    def __init__(
        self, url_repository: UrlRepository, short_code_repository: ShortCodeRepository
    ):
        self.url_repository = url_repository
        self.short_code_repository = short_code_repository

    async def list(self) -> Dict[str, str]:
        return await self.url_repository.list()

    async def get_original_url(self, short_code: str) -> str:
        return await self.url_repository.get(short_code)

    async def shorten(self, long_url: str) -> str:
        short_url_code: str = await self.short_code_repository.short_code()

        payload = {
            "original_url": long_url,
            "short_url_code": short_url_code,
            "created_by": "me@example.com",
        }
        return await self.url_repository.create(payload)
