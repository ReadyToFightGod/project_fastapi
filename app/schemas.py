# Модель книги с использованием Pydantic
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class Book(BaseModel):
    title: str
    author: str
    year: int


class BookInDB(Book):
    id: int

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    user_name: str
    real_name: str
    email: EmailStr


class UserNew(User):
    password: str


class UserInDB(User):
    id: int
    password_hash: str
    registration_date: datetime

    model_config = ConfigDict(from_attributes=True)
