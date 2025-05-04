# Модель книги с использованием Pydantic
from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Book(BaseModel):
    title: str
    author: str
    year: int


class BookInDB(Book):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthData(BaseModel):
    username: str
    password: str


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
    is_moderator: bool

    model_config = ConfigDict(from_attributes=True)


class EntryStatus(StrEnum):
    PLAN_TO_READ = "Plan to read"
    READING = "Reading"
    READ = "Read"
    DROPPED = "Dropped"


class EntryContent(BaseModel):
    status: EntryStatus
    score: int | None = Field(None, ge=0, le=10)
    review: str | None = None


class Entry(EntryContent):
    book_id: int
    user_id: int


class EntryInDB(Entry):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EntryUpdate(EntryContent):
    id: int
