from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import User

users_router = APIRouter(prefix="/users")


@users_router.post("/new-user", status_code=status.HTTP_201_CREATED)
async def add_user(
    user: Annotated[User, Depends()]
) -> dict:
    ...
    return {"ok": True}


@users_router.delete("/delete-user/{user_id}",
                     status_code=status.HTTP_202_ACCEPTED)
async def delete_user(
    user_id: int
) -> dict:
    ...
    return {"ok", True}
