from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserList,
    UserSchema,
    UserSchemaPublic,
)

app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users(
    session: Session = Depends(get_session),
    limit: int = 10,
    offset: int = 0,
):
    db_users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': db_users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )

    return db_user


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaPublic,
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put(
    '/users/{user_id}',
    response_model=UserSchemaPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    return db_user


@app.delete(
    '/users/{user_id}',
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
