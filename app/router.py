# Эндпоинт для добавления книги
from fastapi import APIRouter, HTTPException, status
from typing import Dict

from app.schemas import Book, BookInDB
from app.repository import BooksRepository


router = APIRouter()


# "База данных" - список книг в памяти
books_db: Dict[int, BookInDB] = {}
current_id = 1  # Счетчик для генерации ID


@router.post("/books", status_code=status.HTTP_201_CREATED)
async def add_book(book: Book) -> Dict:
    # global current_id
    # book_in_db = BookInDB(**book.dict(), id=current_id)
    # books_db[current_id] = book_in_db
    # current_id += 1
    book_id = await BooksRepository.add_one(book)
    return {
        "message": "Книга успешно добавлена",
        "book_id": book_id
    }


# Эндпоинт для получения списка всех книг
@router.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books() -> list[BookInDB]:
    books = await BooksRepository.find_all()
    return books


# Эндпоинт для получения книги по ID
@router.get("/books/{book_id}")
async def get_book(book_id: int) -> BookInDB:
    book = await BooksRepository.find_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Книга с id {book_id} не найдена"}
        )
    return book


# Эндпоинт для обновления книги
@router.put("/books/{book_id}")
async def update_book(book_id: int, book: Book) -> Dict:
    if await BooksRepository.find_id(book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Книга с id {book_id} не найдена"}
        )

    await BooksRepository.put_id(book_id, book)
    updated_book = await BooksRepository.find_id(book_id)
    updated_book = BookInDB.model_validate(updated_book)

    return {
        "message": "Книга успешно обновлена",
        "book_id": updated_book
    }


# Эндпоинт для удаления книги
@router.delete("/books/{book_id}")
async def delete_book(book_id: int) -> Dict:
    if await BooksRepository.find_id(book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Книга с id {book_id} не найдена"}
        )
    await BooksRepository.delete_id(book_id)
    return {"message": "Книга удалена"}
