from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException, Path, Request
from httpx import request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Todos
from starlette import status
from routers import auth
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="./templates")
# Initialize fast api app
router = APIRouter(
    prefix = "/todos",
    tags=['todos']
)

# This will now successfully see the Todos class and build the table
Todos.metadata.create_all(bind=engine)

# include router
router.include_router(auth.router)

# get the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length= 100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
        "json_schema_extra": {
            "example" : {
                "title": " change your oil",
                "description": "change your oil every month",
                "priority" : 5,
                "complete" : True
            }
        }
    }
def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###
### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, user: user_dependency, db: db_dependency):
    try:
        if user is None:
            return redirect_to_login()
            
        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        
        return templates.TemplateResponse(
            request=request, 
            name="todo.html", 
            context={"todos": todos, "user": user}
        )
        
    except Exception as e:
        print(f"Redirect Interrupted By: {e}")
        return redirect_to_login()
    
@router.get('/add-todo-page')
async def render_add_todo_page(request: Request, user: user_dependency):  # 1. Renamed function & 2. Added user_dependency
    try:
        if user is None:
            return redirect_to_login()
            
        # 3. Changed context layout to modern FastAPI/Jinja style and name to your add todo layout HTML file
        return templates.TemplateResponse(
            request=request, 
            name="add_todo.html", 
            context={"user": user}
        )
    except Exception as e:
        print(f"Add Todo Page Error: {e}")
        return redirect_to_login()
### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(stus_code=401, detail="Authentication Failed")
    new_todo = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(new_todo)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(stus_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    # update the the todo fields
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    db.add(todo_model)
    db.commit()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(stus_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(stus_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()