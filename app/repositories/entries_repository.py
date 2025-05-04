
from app.database import new_session
from app.schemas import Entry, EntryContent
from app.database import EntriesTable, BooksTable, UsersTable
from .users_repository import check_username_exists
from sqlalchemy import select, delete, update


async def validate_table_id(session, table, table_id) -> bool:
    query = select(table).where(table.id == table_id)
    result = await session.execute(query)
    if result.one_or_none() is None:
        return False
    return True


async def check_book_exists(session, book_id):
    if not await validate_table_id(session, BooksTable, book_id):
        raise ValueError(f"Book with id {book_id} does not exist.")


async def check_entry_exists(session, entry_id):
    if not await validate_table_id(session, EntriesTable, entry_id):
        raise ValueError(f"Entry with id {entry_id} does not exist.")


class EntriesRepository:
    @classmethod
    async def add_entry(cls, username: str, data: Entry) -> int:
        async with new_session() as session:
            await check_book_exists(session, data.book_id)
            await check_username_exists(session, username, True)
            new_entry = EntriesTable(**data.model_dump(), username=username)
            session.add(new_entry)
            await session.flush()
            await session.commit()
            return new_entry.id

    @classmethod
    async def get_entry(cls, entry_id: int) -> EntriesTable:
        async with new_session() as session:
            await check_entry_exists(session, entry_id)
            query = select(EntriesTable).where(EntriesTable.id == entry_id)
            entry = (await session.execute(query)).scalar_one()
            return entry

    @classmethod
    async def get_entries_username(cls, username: str) -> list[EntriesTable]:
        async with new_session() as session:
            await check_username_exists(session, username, True)
            query = select(EntriesTable)\
                .where(EntriesTable.username == username)
            entry = (await session.execute(query)).scalars().all()
            return entry

    @classmethod
    async def get_entry_owner(cls, entry_id) -> str:
        async with new_session() as session:
            await check_entry_exists(session, entry_id)
            query = select(EntriesTable).where(EntriesTable.id == entry_id)
            entry = (await session.execute(query)).scalar_one()
            return entry.username

    @classmethod
    async def delete_entry(cls, entry_id) -> None:
        async with new_session() as session:
            if not await validate_table_id(session, EntriesTable, entry_id):
                raise KeyError(f"Entry with id {entry_id} does not exist.")
            query = delete(EntriesTable).where(EntriesTable.id == entry_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_entry(cls, entry_id: int, data: EntryContent) -> None:
        async with new_session() as session:
            if not await validate_table_id(session, EntriesTable, entry_id):
                raise KeyError(f"Entry with id {entry_id} does not exist.")
            query = update(EntriesTable)\
                .where(EntriesTable.id == entry_id)\
                .values(**data.model_dump())
            await session.execute(query)
            await session.commit()
