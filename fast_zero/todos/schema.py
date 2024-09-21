from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fast_zero.todos.models import TodoState


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoResponse(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoFilter(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[TodoState] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class TodoList(BaseModel):
    todos: list[TodoResponse]


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[TodoState] = None
