from fastapi import Body, FastAPI
app = FastAPI()

@app.get("/")
async def first_api():
    return {"message" : "Hello Sage!"}

BOOKS = [
    {"title": "Title One", "author" : "Author One", "category" : "science"},
    {"title": "Title Two", "author" : "Author Two", "category" : "history"},
    {"title": "Title Three", "author" : "Author Two", "category" : "history"}
]

# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS

# Return a specific book based on title
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

# Return a specific book based on category
@app.get("/books/")
async def read_catgeory_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Return a specific book based on category and author
@app.get("/books/by-author/{book_author}")
async def read_catgeory_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if  book.get('author').casefold() == book_author.casefold() and book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Return a specific book based on author
@app.get("/books/author/{book_author}")
async def read_catgeory_by_query(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if  book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


# create a new book
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# update the book 
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


# delete the book
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
