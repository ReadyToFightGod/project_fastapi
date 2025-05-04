from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.users_repository import UsersRepository
from app.schemas import UserNew, AuthData, UserInDB
from app.auth import create_access_token, get_token_user
from app.config import settings


auth_router = APIRouter(prefix="/auth", tags=["Authentification"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
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


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    auth_data: Annotated[AuthData, Depends()]
) -> dict:
    try:
        authorized = await UsersRepository.authorize_user(auth_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0]
        )
    if authorized:
        auth_token = create_access_token(auth_data.username)
        return {
            "access_token": auth_token,
            "token_type": "bearer"}
    else:
        return {"message": "something went wrong"}


@auth_router.get("/active_user", status_code=status.HTTP_200_OK)
async def get_active_user(token: str) -> UserInDB:
    username = get_token_user(token)
    user_data = await UsersRepository.get_username_data(username)
    return user_data


@auth_router.delete("/active_user",
                    status_code=status.HTTP_202_ACCEPTED)
async def delete_user(token: str) -> dict:
    username = get_token_user(token)
    if username == settings.admin_username:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "Can not delete administrator user")
    await UsersRepository.delete_username(username)
    return {"message": f"Successfully deleted user {username}"}