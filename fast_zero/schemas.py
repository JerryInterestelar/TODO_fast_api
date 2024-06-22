from pydantic import BaseModel, EmailStr


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
