from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Optional
from passlib.context import CryptContext

# --- Configuration du hash des mots de passe ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None

class User(BaseModel):
    id: int
    name: str
    username: str
    password: str
    gender: str

app = FastAPI()
users_db: List[User] = []
books_db: List[Book] = []



### BOOKS

@app.get("/")
def read_root():
    return {"Hello":  "World"}

@app.get("/api-endpoint")
def first_api():
    return {"message": "Hello"}

@app.get("/books")
async def read_all_books():
    all_books = [book for book in books_db]
    return all_books

@app.get("/books/mybook")
async def read_all_books():
    return {'book_title': 'My favorite book'}

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic_param': dynamic_param}


@app.post("/books/create_book")
async def create_book(new_book: Book):
    new_book.id = len(books_db) + 1 #Simple way to generate an ID
    books_db.append(new_book)
    return {'message': 'Book created succesfully', 'book': new_book}

@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if (book.id == book_id):
            updated_book.id = book_id
            books_db[i] = updated_book
            return {'message': f'Book with ID {book_id} has been updated', 'book': updated_book}
    raise HTTPException(status_code=404, detail = f'Book with ID {book_id} not found')

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if (book.id == book_id):
            del books_db[i]
            return {'message': f'Book with ID {book_id} has been deleted'}
    raise HTTPException(status_code=404, detail = f'Book with ID {book_id} not found')

@app.patch("/books/patch/{book_id}")
async def patch_book(book_id: int, patch_data: Book):
    stored_book_data = None
    for book in books_db:
        if (book.id == book_id):
            stored_book_data = book
            update_data = patch_data.dict(exclude_unset = True)
            updated_book = stored_book_data.copy(update = update_data)
            books_db[books_db.index(book)] = updated_book
            return {'message': f'Book with ID {book_id} has been patched', 'book': updated_book}
    if (stored_book_data is None):
        raise HTTPException(status_code=404, detail = f'Book with ID {book_id} not found')



### USERS

@app.post("/users/create_user")
async def create_user(new_user: User):
    if any(user.username == new_user.username for user in users_db):
        raise HTTPException(status_code=404, detail="Username already exists")
    else:
        new_user.id = len(users_db) + 1 # Simple way to generate an ID
        new_user.password = get_password_hash(new_user.password)
        users_db.append(new_user)
        return {'message': 'User created succesfully', 'user': new_user}

@app.put("/users/update_users/{user_id}")
async def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if (user.id == user_id):
            updated_user.id = user_id
            users_db[i] = updated_user
            return {'message': f'User with ID {user_id} has been updated', 'user': updated_user}
    raise HTTPException(status_code=404, detail = f'User with ID {user_id} not found')

@app.delete("/users/delete_user/{user_id}")
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if (user.id == user_id):
            del users_db[i]
            return {'message': f'User with ID {user_id} has been deleted'}
    raise HTTPException(status_code=404, detail = f'User with ID {user_id} not found')

@app.patch("/users/patch/{user_id}")
async def patch_user(user_id: int, patch_data: User):
    stored_user_data = None
    for user in users_db:
        if (user.id == user_id):
            stored_user_data = user
            update_data = patch_data.dict(exclude_unset = True)
            updated_user = stored_user_data.copy(update = update_data)
            users_db[users_db.index(user)] = updated_user
            return {'message': f'User with ID {user_id} has been patched', 'user': update_user}
    if (stored_user_data is None):
        raise HTTPException(status_code=404, detail = f'User with ID {user_id} not found')

@app.post("/users/connect/")
async def connect_user(user_name: str, user_password: str):
    for user in users_db:
        if (user.username == user_name and verify_password(user_password, user.password) == True):
            return {'message': 'User is connected', 'user': update_user}
    return {'message': 'Wrong username or password'}