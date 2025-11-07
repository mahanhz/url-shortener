from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapter.incoming import urls
from src.adapter.outgoing.database import create_db_and_tables, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("starting up...")
    await create_db_and_tables()
    yield
    # Shutdown code
    print("shutting down...")
    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(urls.router)
