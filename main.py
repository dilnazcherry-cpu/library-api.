
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Library Books API")


# Модель данных книги
class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=0, le=2100)


class Book(BookCreate):
    id: int


# Хранилище книг в памяти
books: list[Book] = []
next_id = 1


# GET: получить все книги
@app.get("/books")
def get_books():
    return books


# GET: получить книгу по ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


# POST: добавить новую книгу
@app.post("/books", status_code=201)
def create_book(book_data: BookCreate):
    global next_id

    book = Book(id=next_id, **book_data.model_dump())
    books.append(book)
    next_id += 1

    return book


# PUT: обновить книгу
@app.put("/books/{book_id}")
def update_book(book_id: int, book_data: BookCreate):
    for index, book in enumerate(books):
        if book.id == book_id:
            updated_book = Book(
                id=book_id,
                **book_data.model_dump()
            )
            books[index] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Книга не найдена")


# DELETE: удалить книгу
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted_book = books.pop(index)
            return {
                "message": "Книга удалена",
                "book": deleted_book
            }

    raise HTTPException(status_code=404, detail="Книга не найдена")