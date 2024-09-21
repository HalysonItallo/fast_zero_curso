from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from fast_zero.todos.models import Todo
from fast_zero.todos.schema import TodoFilter, TodoList, TodoResponse, TodoSchema, TodoUpdate
from fast_zero.types import T_CurrentUser, T_Session

todo_router = APIRouter(prefix="/todos", tags=["todos"])


@todo_router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoSchema, session: T_Session, user: T_CurrentUser):
    db_todo = Todo(
        **todo.model_dump(exclude=("user_id",)),
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@todo_router.get("/", response_model=TodoList)
def list_todo(session: T_Session, user=T_CurrentUser, todo_filter: TodoFilter = Depends()):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(Todo.description.contains(todo_filter.description))

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = session.scalars(query.offset(todo_filter.offset).limit(todo_filter.limit)).all()

    return {"todos": todos}


@todo_router.patch("/{todo_id}", response_model=TodoResponse)
def patch_user(
    todo_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
    new_todo: TodoUpdate,
):
    exist_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id),
    )

    if not exist_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    for key, value in new_todo.model_dump(exclude_unset=True).items():
        setattr(exist_todo, key, value)

    session.add(exist_todo)
    session.commit()
    session.refresh(exist_todo)

    return exist_todo


@todo_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(todo_id: int, session: T_Session, current_user: T_CurrentUser):
    exist_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id),
    )

    if not exist_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    session.delete(exist_todo)
    session.commit()
