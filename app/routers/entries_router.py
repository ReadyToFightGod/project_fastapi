from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import Entry, EntryContent, EntryInDB
from app.auth import get_token_user
from app.repositories.entries_repository import EntriesRepository
from app.repositories.users_repository import UsersRepository

entries_router = APIRouter(prefix="/entries", tags=["Entries"])


@entries_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_entry(
    token: str,
    entry: Annotated[Entry, Depends()]
) -> dict:
    username = get_token_user(token)
    try:
        entry_id = await EntriesRepository.add_entry(username, entry)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args[0],
        )
    return {"Entry id": entry_id}


@entries_router.get("/{entry_id}", status_code=status.HTTP_200_OK)
async def get_entry(entry_id: int) -> EntryInDB:
    try:
        entry = await EntriesRepository.get_entry(entry_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    return EntryInDB.model_validate(entry)


@entries_router.get("/user/{username}", status_code=status.HTTP_200_OK)
async def get_user_entries(username: str) -> list[EntryInDB]:
    try:
        entries = await EntriesRepository.get_entries_username(username)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    return [EntryInDB.model_validate(entry) for entry in entries]


@entries_router.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_entries(book_id: int) -> list[EntryInDB]:
    try:
        entries = await EntriesRepository.get_entries_book_id(book_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    return [EntryInDB.model_validate(entry) for entry in entries]


@entries_router.delete("/{entry_id}", status_code=status.HTTP_202_ACCEPTED)
async def delte_entry(token: str, entry_id: int) -> dict:
    token_user = get_token_user(token)
    try:
        entry_user = await EntriesRepository.get_entry_owner(entry_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    if ((token_user != entry_user)
            and (not await UsersRepository.username_is_moderator(token_user))):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "You are not permitted to modify this entry")
    await EntriesRepository.delete_entry(entry_id)
    return {"message": f"Entry with id {entry_id} deleted"}


@entries_router.patch("/{entry_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_entry(
    token: str,
    entry_id: int,
    data: Annotated[EntryContent, Depends()],
) -> dict:
    token_user = get_token_user(token)
    try:
        entry_user = await EntriesRepository.get_entry_owner(entry_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    if ((token_user != entry_user)
            and (not await UsersRepository.username_is_moderator(token_user))):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "You are not permitted to modify this entry")
    await EntriesRepository.update_entry(entry_id, data)
    return {"message": f"Entry with id {entry_id} updated"}
