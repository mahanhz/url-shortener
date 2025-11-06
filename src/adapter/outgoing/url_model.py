from datetime import datetime

from sqlmodel import SQLModel, Field


class UrlTableModel(SQLModel, table=True):
    __tablename__ = "urls"
    id: int | None = Field(default=None, primary_key=True)
    short_url_code: str = Field(index=True)
    original_url: str
    creation_time: datetime = Field(default_factory=lambda: datetime.now())
    created_by: str | None
    expiration_time: datetime | None
