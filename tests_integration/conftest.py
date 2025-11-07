import os

from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from tests_integration.db_setup import create_table

# Start the containers
redis_container = RedisContainer("redis:8.2-alpine")
redis_container.start()

postgres_container = PostgresContainer("postgres:16-alpine")
postgres_container.start()

# Set environment variables *before* app imports anything
os.environ["REDIS_HOST"] = redis_container.get_container_host_ip()
os.environ["REDIS_PORT"] = str(redis_container.get_exposed_port(6379))

os.environ["DB_CONN"] = postgres_container.get_connection_url()
os.environ["DB_HOST"] = postgres_container.get_container_host_ip()
os.environ["DB_PORT"] = str(postgres_container.get_exposed_port(5432))
os.environ["DB_USERNAME"] = postgres_container.username
os.environ["DB_PASSWORD"] = postgres_container.password
os.environ["DB_NAME"] = postgres_container.dbname
os.environ["DATABASE_URL"] = (
    f"postgresql+asyncpg://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

create_table()


def pytest_sessionfinish(session, exitstatus):
    """Stop container when pytest finishes."""
    postgres_container.stop()
    redis_container.stop()
