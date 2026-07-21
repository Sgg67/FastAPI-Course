from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Todos
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
# Initialize fast api app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allows all origins (including your Codespace domain)
    allow_credentials=True,
    allow_methods=["*"],          # Allows GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],          # Allows all headers
)

# This will now successfully see the Todos class and build the table
Todos.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory = "./static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
@app.get("/healthy")
def health_check():
    return {'status' : 'Healthy'}

# include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)