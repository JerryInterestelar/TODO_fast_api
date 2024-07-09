from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserList,
    UserSchema,
    UserSchemaPublic,
)
from fast_zero.security import (
    get_current_user,
    get_password_hash,
    get_session,
)

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users(
    session: Session,
    limit: int = 10,
    offset: int = 0,
):
    db_users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': db_users}


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def read_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )

    return db_user


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaPublic,
)
def create_user(
    user: UserSchema,
    session: Session,
):
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
        password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put(
    '/{user_id}',
    response_model=UserSchemaPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete(
    '/{user_id}',
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
