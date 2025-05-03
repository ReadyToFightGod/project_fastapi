from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.users_repository import UsersRepository
from app.routers.users_router import users_router
from app.schemas import UserNew, AuthData


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


@auth_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login_user(
    auth_data: AuthData
) -> dict:
    try:
        authorized = await UsersRepository.authorize_user(auth_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0]
        )
    if authorized:
        return {"message": "your are authorized"}
    else:
        return {"message": "something went wrong"}


@auth_router.delete("/{user_id}",
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