import pytest
from unittest.mock import AsyncMock  # ← replace with actual import path

from src.application.service.url_shortening_service import UrlShorteningService


@pytest.fixture
def mock_url_repository():
    """Creates a mocked async UrlRepository."""
    mock_repo = AsyncMock()
    mock_repo.list.return_value = {
        "yui123": "https://example.com",
        "abc789": "https://openai.com",
    }
    mock_repo.get.return_value = "https://example.com/yui123"
    mock_repo.create.return_value = "yui123"
    return mock_repo


@pytest.fixture
def mock_short_code_repository():
    """Creates a mocked async ShortCodeRepository."""
    mock_repo = AsyncMock()
    mock_repo.short_code.return_value = "q0VSiWkf"
    return mock_repo


@pytest.fixture
def service(mock_url_repository, mock_short_code_repository):
    """Injects the mocked repository into the service."""
    return UrlShorteningService(mock_url_repository, mock_short_code_repository)


@pytest.mark.asyncio
async def test_list(service, mock_url_repository):
    # When
    result = await service.list()

    # Then
    mock_url_repository.list.assert_awaited_once()
    assert isinstance(result, dict)
    assert result["yui123"] == "https://example.com"


@pytest.mark.asyncio
async def test_get_original_url(service, mock_url_repository):
    # When
    result = await service.get_original_url("yui123")

    # Then
    mock_url_repository.get.assert_awaited_once_with("yui123")
    assert result == "https://example.com/yui123"


@pytest.mark.asyncio
async def test_shorten(service, mock_url_repository):
    # Given
    long_url = "https://example.com/long"

    # When
    result = await service.shorten(long_url)

    # Then
    mock_url_repository.create.assert_awaited_once()
    args, _ = mock_url_repository.create.call_args
    payload = args[0]

    assert payload["original_url"] == long_url
    assert payload["short_url_code"] == "q0VSiWkf"
    assert payload["created_by"] == "me@example.com"
    assert result == "yui123"
