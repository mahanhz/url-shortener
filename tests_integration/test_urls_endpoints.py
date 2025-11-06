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

postgres = PostgresContainer("postgres:16-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname

    create_table()

    test_database_url = f"postgresql+asyncpg://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    os.environ["DATABASE_URL"] = test_database_url
    importlib.reload(database)  # forces re-import with new env var


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    delete_all_urls()


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
