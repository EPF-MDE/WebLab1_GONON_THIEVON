from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
from typing import Optional, List

class Book(BaseModel):
    id: Optional[int] = None
    title: str 
    author: str
    category: Optional[str] = None
    publication_year: Optional[int] = None

class User:
    id: int
    name: str
    username: str
    password: str
    gender: str

app = FastAPI()
books_db: List[Book] = []
users_db: List[User] = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books")
async def read_all_books():
    return {"message": "list of books"}

@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "my favorite book"}

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {"dynamic_param": dynamic_param}

@app.post("/books/create_book")
async def create_book(new_book: Book):
    new_book.id = len(books_db) + 1
    books_db.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[i] = updated_book
            return {"message": f"Book with id {book_id} updated successfully", "book": updated_book}
    raise HTTPException(status_code=404, detail="Book with id {book_id} not found")

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[i]
            return {"message": f"Book with id {book_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Book with id {book_id} not found")

@app.patch("/books/update_book/{book_id}")
async def patch_book(book_id: int, patch_data: Book):
    stored_book_data = None
    for book in books_db:
        if book.id == book_id:
            stored_book_data = book
            update_data = patch_data.dict(exclude_unset=True)
            updated_book = stored_book_data.copy(update=update_data)
            books_db[books_db.index(book)] = updated_book
            return {"message": f"Book with id {book_id} patched successfully", "book": updated_book}
    if stored_book_data is None:
        raise HTTPException(status_code=404, detail="Book with id {book_id} not found")

@app.post("/users/create_user")
async def create_user(new_user: User):
    new_user.id = len(users_db) + 1
    users_db.append(new_user)
    return {"message": "User created successfully", "user": new_user}


@app.post("/users/login")
async def login_user(credentials: username):
    # Recherche de l'utilisateur par username
    user = next((user for user in users_db if user.username == credentials.username), None)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérification du mot de passe
    if user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    
    return {"message": "Connexion réussie", "user": user}
