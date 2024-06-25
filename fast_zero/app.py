from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserSchema,
    UserSchemaPublic,
)

app = FastAPI()

# banco de dados provisório
database = []


@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users():
    return {'users': database}

@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )
    user_with_id = database[user_id - 1]
    return user_with_id

@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaPublic,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id


@app.put(
    '/users/{user_id}',
    response_model=UserSchemaPublic,
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    response_model=Message,
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User Not Found',
        )
    del database[user_id - 1]
    return {'message': 'User deleted'}
