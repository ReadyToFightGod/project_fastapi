from fastapi import APIRouter, HTTPException, status

from app.schemas import UserInDB
from app.repositories.users_repository import UsersRepository
from app.auth import get_token_user

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/")
async def get_users_list() -> list[dict]:
    users_list = await UsersRepository.get_username_list()
    return users_list


@users_router.post("/promote", status_code=status.HTTP_202_ACCEPTED)
async def get_user(moderator_token: str,
                   username: str,
                   promote: bool = True) -> dict:
    if username == "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Administrator user can't be promoted or demoted")
    mod_name = get_token_user(moderator_token)
    is_moderator = await UsersRepository.username_is_moderator(mod_name)
    if not is_moderator:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You are not a moderator."
        )
    try:
        await UsersRepository.set_username_moderator(username, promote)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.args[0])
    return {"message": f"User {username} " + ("promoted to moderator."
                                              if promote else
                                              "demoted from moderator.")}
