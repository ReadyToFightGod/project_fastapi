from app.database import new_session
from app.schemas import Book, BookStats, EntryStatus, EntryInDB
from app.database import BooksTable
from app.repositories.entries_repository import EntriesRepository
from sqlalchemy import select, delete, update


class BooksRepository:
    @classmethod
    async def add_one(cls, data: Book) -> int:
        async with new_session() as session:
            book_dict = data.model_dump()
            book = BooksTable(**book_dict)
            session.add(book)
            await session.flush()
            await session.commit()
            return book.id

    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(BooksTable)
            result = await session.execute(query)
            book_models = result.scalars().all()
            return book_models

    @classmethod
    async def find_id(cls, id: int) -> BooksTable | None:
        async with new_session() as session:
            query = select(BooksTable).filter(BooksTable.id == id)
            result = await session.execute(query)
            book_model = result.scalar_one_or_none()
            return book_model

    @classmethod
    async def delete_id(cls, book_id: int) -> None:
        async with new_session() as session:
            query = delete(BooksTable).where(BooksTable.id == book_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def put_id(cls, id: int, data: Book) -> None:
        async with new_session() as session:
            print(data)
            query = update(BooksTable)\
                .where(BooksTable.id == id)\
                .values(**data.model_dump())
            print(query)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_book_stats(cls, book_id: int) -> None:
        entries = await EntriesRepository.get_entries_book_id(book_id)
        new_stats = BookStats()
        score_sum = 0
        for entry in entries:
            entry = EntryInDB.model_validate(entry)
            new_stats.entries += 1
            if entry.score is not None:
                new_stats.ratings += 1
                score_sum += entry.score
            if entry.review is not None:
                new_stats.reviews += 1
            match entry.status:
                case EntryStatus.PLAN_TO_READ:
                    new_stats.plan_to_read += 1
                case EntryStatus.READING:
                    new_stats.reading += 1
                case EntryStatus.READ:
                    new_stats.read += 1
                case EntryStatus.DROPPED:
                    new_stats.dropped += 1
        new_stats.mean_score = score_sum / new_stats.ratings
        return new_stats
