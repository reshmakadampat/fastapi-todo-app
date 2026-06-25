from fastapi import FastAPI, Depends, Header, HTTPException , Request 
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from database import engine, SessionLocal
from models import Base, User, Todo
from schemas import UserCreate, UserLogin, TodoCreate
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM)
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)
@app.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )
@app.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(
        authorization: str = Header(None),
        db: Session = Depends(get_db)
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@app.get("/")
def home():
    return {"message": "Todo App API is running!"}


@app.post("/register")
def register(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {"message": "Email already registered"}

    # Hash password
    hashed_password = hash_password(user.password)

    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }
@app.post("/login")
def login(
        user: UserLogin,
        db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {
            "message": "Invalid email or password"
        }

    if not verify_password(
            user.password,
            existing_user.password
    ):
        return {
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {"user_id": existing_user.id}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.post("/todos")
def create_todo(
        todo: TodoCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    new_todo = Todo(
    title=todo.title,
    description=todo.description,
    user_id=current_user.id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {
        "message": "Todo created successfully"
    }
@app.get("/todos")
def get_todos(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    todos = db.query(Todo).filter(
        Todo.user_id == current_user.id
    ).all()

    return todos
@app.put("/todos/{todo_id}")
def update_todo(
        todo_id: int,
        todo: TodoCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    existing_todo = db.query(Todo).filter(
    Todo.id == todo_id,
    Todo.user_id == current_user.id
    ).first()

    if not existing_todo:
        return {"message": "Todo not found"}

    existing_todo.title = todo.title
    existing_todo.description = todo.description

    db.commit()

    return {
        "message": "Todo updated successfully"
    }
@app.delete("/todos/{todo_id}")
def delete_todo(
        todo_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    existing_todo = db.query(Todo).filter(
    Todo.id == todo_id,
    Todo.user_id == current_user.id
    ).first()

    if not existing_todo:
        return {
            "message": "Todo not found"
        }

    db.delete(existing_todo)
    db.commit()

    return {
        "message": "Todo deleted successfully"
    }
