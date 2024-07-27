from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    Message,
    TodoList,
    TodoSchema,
    TodoSchemaPublic,
    TodoUpdate,
)
from fast_zero.security import get_current_user

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', response_model=TodoSchemaPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session,
):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(  # noqa
    session: Session,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoSchemaPublic)
def patch_todo(
    todo_id: int, session: Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, user.id == Todo.user_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: CurrentUser):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id, user.id == Todo.user_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task has been deleted successfully'}
