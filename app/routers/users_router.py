from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import UserNew, UserInDB
from app.repositories.users_repository import UsersRepository

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user(
    user: Annotated[UserNew, Depends()]
) -> dict:
    try:
        user_id = await UsersRepository.add_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT,
            detail=e.args[0],
        )
    return {"user_id": user_id}


@users_router.get("/")
async def get_users_list() -> list[dict]:
    users_list = await UsersRepository.get_username_list()
    return users_list


@users_router.get("/{user_id}")
async def get_user(user_id: int) -> UserInDB:
    user_data = await UsersRepository.get_user_data(user_id)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"User with id {user_id} does not exits."}
        )
    return user_data


@users_router.delete("/{user_id}",
                     status_code=status.HTTP_202_ACCEPTED)
async def delete_user(
    user_id: int
) -> dict:
    if await UsersRepository.get_user_data(user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"User with id {user_id} does not exits."}
        )
    await UsersRepository.delete_user(user_id)
    return {"message": f"Successfully deleted user with id {user_id}"}
