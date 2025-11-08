import pytest

from src.adapter.outgoing.redis_short_code_repository import base62_short_code


@pytest.mark.asyncio
async def test_billion_short_code_has_length_of_8():
    result = base62_short_code(1_000_000_000)

    assert len(result) == 8


@pytest.mark.asyncio
async def test_trillion_short_code_has_length_of_8():
    result = base62_short_code(1_000_000_000_000)

    assert len(result) == 8
