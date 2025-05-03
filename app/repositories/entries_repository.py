
from app.database import new_session
from app.schemas import Entry, EntryContent
from app.database import EntriesTable, BooksTable, UsersTable
from sqlalchemy import select, delete, update


async def validate_table_id(session, table, table_id) -> bool:
    query = select(table).where(table.id == table_id)
    result = await session.execute(query)
    if result.one_or_none() is None:
        return False
    return True


class EntriesRepository:
    @classmethod
    async def add_entry(cls, data: Entry) -> int:
        async with new_session() as session:
            if not await validate_table_id(session, BooksTable, data.book_id):
                raise KeyError(f"Book with id {data.book_id} does not exist.")
            if not await validate_table_id(session, UsersTable, data.user_id):
                raise KeyError(f"User with id {data.user_id} does not exist.")
            new_entry = EntriesTable(**data.model_dump())
            session.add(new_entry)
            await session.flush()
            await session.commit()
            return new_entry.id

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
