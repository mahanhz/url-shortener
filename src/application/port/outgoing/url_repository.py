from typing import Dict


class UrlRepository:
    async def list(self) -> Dict[str, str]:
        pass

    async def get(self, short_code: str) -> str:
        pass

    async def create(self, payload: dict) -> str:
        pass
