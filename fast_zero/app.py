from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import UserDB, UserList, UserSchema, UserSchemaPublic

app = FastAPI()

# banco de dados provisório
database = []


@app.get('/')
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users():
    return {'users': database}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaPublic,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id
