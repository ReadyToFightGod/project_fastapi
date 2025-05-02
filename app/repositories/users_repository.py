from app.database import new_session
from app.schemas import User, UserInDB
from app.database import UsersTable
from sqlalchemy import select, delete, update


class BooksRepository:
    @classmethod
    async def add_user(data: User):
        ...

    @classmethod
    async def delete_user(user_id: int):
        ...
