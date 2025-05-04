# Эндпоинт для добавления книги
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.schemas import Book, BookInDB
from app.repositories.books_repository import BooksRepository
from app.repositories.users_repository import UsersRepository
from app.auth import get_token_user


books_router = APIRouter(prefix="/books", tags=["Books"])


async def check_token_is_mod(token):
    is_mod = await UsersRepository.username_is_moderator(get_token_user(token))
    if not is_mod:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "You are not permitted to modify books list.")


@books_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book(
    token: str,
    book: Annotated[Book, Depends()]
) -> dict:
    await check_token_is_mod(token)
    book_id = await BooksRepository.add_one(book)
    return {
        "message": "Book successfully added",
        "book_id": book_id
    }


@books_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_books() -> list[BookInDB]:
    books = await BooksRepository.find_all()
    return books


@books_router.get("/{book_id}")
async def get_book(book_id: int) -> BookInDB:
    book = await BooksRepository.find_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Book with id {book_id} was not found"}
        )
    return book


@books_router.put("/{book_id}")
async def update_book(
    token: str,
    book_id: int,
    book: Annotated[Book, Depends()]
) -> dict:
    await check_token_is_mod(token)
    if await BooksRepository.find_id(book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Book with id {book_id} was not found."}
        )

    await BooksRepository.put_id(book_id, book)
    updated_book = await BooksRepository.find_id(book_id)
    updated_book = BookInDB.model_validate(updated_book)

    return {
        "message": "Book successfully updated.",
        "book_id": updated_book
    }


@books_router.delete("/{book_id}")
async def delete_book(token: str, book_id: int) -> dict:
    await check_token_is_mod(token)
    if await BooksRepository.find_id(book_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Book with id {book_id} was not found."}
        )
    await BooksRepository.delete_id(book_id)
    return {"message": "Book deleted"}
