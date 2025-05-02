from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import Entry, EntryContent
from app.repositories.entries_repository import EntriesRepository

entries_router = APIRouter(prefix="/entries", tags=["Entries"])


@entries_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_entry(
    entry: Annotated[Entry, Depends()]
) -> dict:
    try:
        entry_id = await EntriesRepository.add_entry(entry)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args[0],
        )
    return {"Entry id": entry_id}


@entries_router.delete("/{entry_id}", status_code=status.HTTP_202_ACCEPTED)
async def delte_entry(entry_id: int) -> dict:
    try:
        await EntriesRepository.delete_entry(entry_id)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args[0],
        )
    return {"message": f"Entry with id {entry_id} deleted"}

@entries_router.patch("/{entry_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_entry(
    entry_id: int, data: Annotated[EntryContent, Depends()]
) -> dict:
    try:
        await EntriesRepository.update_entry(entry_id, data)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.args[0],
        )
    return {"message": f"Entry with id {entry_id} updated"}
