import string
from typing import Dict

import shortuuid

from src.application.port.incoming.ShorteningService import ShorteningService
from src.application.port.outgoing.url_repository import UrlRepository


alphabet = string.ascii_lowercase + string.digits
su = shortuuid.ShortUUID(alphabet=alphabet)


class UrlShorteningService(ShorteningService):
    def __init__(self, url_repository: UrlRepository):
        self.url_repository = url_repository

    async def list(self) -> Dict[str, str]:
        return await self.url_repository.list()

    async def get_original_url(self, short_code: str) -> str:
        return await self.url_repository.get(short_code)

    async def shorten(self, long_url: str) -> str:
        short_url_code: str = su.random(length=8)

        payload = {
            "original_url": long_url,
            "short_url_code": short_url_code,
            "created_by": "me@example.com",
        }
        return await self.url_repository.create(payload)
