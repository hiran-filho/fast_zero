from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):  # type: ignore
    username: str
    email: EmailStr
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UserPublic):
    updated_at: datetime


class UserList(BaseModel):
    users: list[UserPublic]
