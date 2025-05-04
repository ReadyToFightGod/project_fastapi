import string
from app.auth import get_password_hash, verify_password
from app.database import new_session
from app.schemas import UserNew, UserInDB, AuthData
from app.database import UsersTable
from sqlalchemy import select, delete, update
from datetime import datetime


ALLOWED_USERNAME_LETTERS = set(string.ascii_letters + string.digits + "-_")


async def check_username_exists(session, username: str,
                                should_exist: bool):
    query = select(UsersTable).where(UsersTable.user_name == username)
    result = (await session.execute(query)).scalar_one_or_none()
    exists = result is not None
    if exists and not should_exist:
        raise ValueError(f"User with name {username} already exists.")
    elif should_exist and not exists:
        raise ValueError(f"User with name {username} does not exist.")


def check_username_correct(username: str) -> bool:
    illegal_letters = set(username) - ALLOWED_USERNAME_LETTERS
    if illegal_letters == set():
        return
    raise ValueError("Username contains disallowed letters: "
                     + ",".join([f"'{v}'" for v in illegal_letters]))


class UsersRepository:
    @classmethod
    async def add_user(csl, data: UserNew) -> int:
        async with new_session() as session:
            check_username_correct(data.user_name)
            await check_username_exists(session, data.user_name, False)
            user_dict = data.model_dump()
            user_dict["password_hash"] = get_password_hash(data.password)
            del user_dict["password"]
            user_dict["registration_date"] = datetime.now()
            new_user = UsersTable(**user_dict)
            session.add(new_user)
            await session.flush()
            await session.commit()
            return new_user.id

    @classmethod
    async def authorize_user(cls, data: AuthData) -> bool:
        async with new_session() as session:
            query = select(UsersTable)\
                .where(UsersTable.user_name == data.username)
            user = (await session.execute(query)).scalar_one_or_none()
            if user is None:
                raise ValueError(
                    f"User with name {data.username} does not exist.")
            if verify_password(data.password, user.password_hash):
                return True
            else:
                raise ValueError(
                    f"Wrong password for user {data.username}")

    @classmethod
    async def set_username_moderator(cls, username: str, is_moderator: bool):
        async with new_session() as session:
            await check_username_exists(session, username, True)
            query = update(UsersTable)\
                .where(UsersTable.user_name == username)\
                .values(is_moderator=is_moderator)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def username_is_moderator(cls, username: str) -> bool:
        async with new_session() as session:
            await check_username_exists(session, username, True)
            query = select(UsersTable)\
                .where(UsersTable.user_name == username)
            user = (await session.execute(query)).scalar_one()
            return user.is_moderator

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
            return UserInDB.model_validate(user_data)

    @classmethod
    async def get_username_data(cls, username: str) -> UserInDB:
        async with new_session() as session:
            await check_username_exists(session, username, True)
            query = select(UsersTable).where(UsersTable.user_name == username)
            result = await session.execute(query)
            user_data = result.scalar_one_or_none()
            return UserInDB.model_validate(user_data)

    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with new_session() as session:
            query = delete(UsersTable).where(UsersTable.id == user_id)
            print(query)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_username(cls, username: str) -> None:
        async with new_session() as session:
            query = delete(UsersTable).where(UsersTable.user_name == username)
            print(query)
            await session.execute(query)
            await session.commit()
