from fastapi import APIRouter, HTTPException, status

from app.schemas import UserInDB
from app.repositories.users_repository import UsersRepository

users_router = APIRouter(prefix="/users", tags=["Users"])


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
