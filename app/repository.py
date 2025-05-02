from app.database import new_session
from app.schemas import Book
from app.database import BooksTable
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
