import importlib

from fastapi.testclient import TestClient

from src.main import app

import os
import pytest
from testcontainers.postgres import PostgresContainer

from src.adapter.outgoing import database
from tests_integration.db_setup import (
    create_table,
    delete_all_urls,
    create_a_shortened_url,
)


client = TestClient(app)


def test_get_all_urls(monkeypatch):
    create_a_shortened_url(short_code="werlO53k", orig_url="https://www.google.com")

    response = client.get("/urls")
    assert response.status_code == 200
    assert response.json() == {"werlO53k": "https://www.google.com"}


def test_get_short_url():
    create_a_shortened_url(short_code="nbsfu87d", orig_url="https://www.gmail.com")

    response = client.get("/urls/nbsfu87d", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://www.gmail.com"


def test_create_short_url():
    base_url = "http://testserver/urls/"
    response = client.post("/urls", json={"url": "https://www.bbc.com"})
    assert response.status_code == 201

    short_url = str(response.json())
    assert short_url.startswith(base_url)
    assert len(short_url) - len(base_url) == 8, (
        "URL must end with 8-character short code"
    )
