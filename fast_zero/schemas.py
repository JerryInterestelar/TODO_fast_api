from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserSchemaPublic]
