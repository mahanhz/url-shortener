import pytest

from src.domain.model.url import OriginalUrl, ShortenedUrl


def test_original_url_valid():
    url = OriginalUrl("https://example.com")
    assert url.value == "https://example.com"


def test_original_url_none():
    with pytest.raises(ValueError) as excinfo:
        OriginalUrl(None)
    assert str(excinfo.value) == "A value must be provided"


def test_shortened_url_valid():
    url = ShortenedUrl("abc123")
    assert url.value == "abc123"


def test_shortened_url_none():
    with pytest.raises(ValueError) as excinfo:
        ShortenedUrl(None)
    assert str(excinfo.value) == "A value must be provided"
