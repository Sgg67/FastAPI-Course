from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Todos
from routers import auth, todos, admin, users
from routers.auth import get_current_user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Todos.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def test(request: Request):
    try:
        user = await get_current_user(request)
        if user is None:
            return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    except HTTPException:
        return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)