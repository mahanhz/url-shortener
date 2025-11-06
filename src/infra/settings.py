from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    DATABASE_URL: str

    class Config:
        env_file = ".env"
