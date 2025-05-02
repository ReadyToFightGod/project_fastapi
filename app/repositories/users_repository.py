from app.database import new_session
from app.schemas import UserNew, UserInDB
from app.database import UsersTable
from sqlalchemy import select, delete, update
from hashlib import sha256
from datetime import datetime


class UsersRepository:
    @classmethod
    async def add_user(csl, data: UserNew) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()
            user_dict["password_hash"] = \
                sha256(bytes(user_dict["password"], encoding="utf8"))\
                .hexdigest()
            del user_dict["password"]
            user_dict["registration_date"] = datetime.now()
            new_user = UsersTable(**user_dict)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.id

    @classmethod
    async def get_username_list(cls) -> list[dict]:
        async with new_session() as session:
            query = select(UsersTable)
            result = await session.execute(query)
            username_list = [
                {"id": user.id, "user_name": user.user_name}
                for user in result.scalars().all()
            ]
            return username_list

    @classmethod
    async def get_user_data(cls, user_id: int) -> UserInDB | None:
        async with new_session() as session:
            query = select(UsersTable).where(UsersTable.id == user_id)
            result = await session.execute(query)
            user_data = result.scalar_one_or_none()
            if user_data is None:
                return None
            print(user_data.__dict__)
            return UserInDB.model_validate(user_data)

    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with new_session() as session:
            query = delete(UsersTable).where(UsersTable.id == user_id)
            print(query)
            await session.execute(query)
            await session.commit()
