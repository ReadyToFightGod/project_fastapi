from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.database import create_tables, delete_tables
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Database was cleared")
    await create_tables()
    print("Database ready for work")
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
