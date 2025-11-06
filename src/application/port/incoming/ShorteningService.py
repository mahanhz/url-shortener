from typing import Dict


class ShorteningService:
    async def list(self) -> Dict[str, str]:
        pass

    async def shorten(self, long_url: str) -> str:
        pass

    async def get_original_url(self, short_code: str) -> str:
        pass
