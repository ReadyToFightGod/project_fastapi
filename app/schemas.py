# Модель книги с использованием Pydantic
from pydantic import BaseModel, ConfigDict


class Book(BaseModel):
    title: str
    author: str
    year: int


class BookInDB(Book):
    id: int

    model_config = ConfigDict(from_attributes=True)
