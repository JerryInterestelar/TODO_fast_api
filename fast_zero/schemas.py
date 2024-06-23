from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    # Tem tudo que UserSchema tem
    id: int


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: str


class UserList(BaseModel):
    users: list[UserSchemaPublic]
