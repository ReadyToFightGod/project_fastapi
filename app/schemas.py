# Модель книги с использованием Pydantic
from datetime import date
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
    password: str


class UserInDB(User):
    id: int
    registration_date: date

    model_config = ConfigDict(from_attributes=True)
