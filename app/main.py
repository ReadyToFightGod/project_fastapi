from fastapi import FastAPI

from contextlib import asynccontextmanager
from app.repositories.users_repository import UsersRepository
from app.schemas import UserNew
from app.database import create_tables, delete_tables
from app.routers.books_router import books_router
from app.routers.users_router import users_router
from app.routers.entries_router import entries_router
from app.routers.auth_router import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Database was cleared")
    await create_tables()
    print("Database ready for work")
    admin = UserNew(
        user_name="admin",
        real_name="Administrator",
        email="admin@admin.com",
        password="admin")
    try:
        await UsersRepository.add_user(admin)
    except ValueError:
        pass
    await UsersRepository.set_username_moderator("admin", True)
    yield
    print("Turning off")


app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
app.include_router(users_router)
app.include_router(entries_router)
app.include_router(auth_router)
