from typing import List

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    telegram_id: int

    class Config:
        orm_mode = True


class UserOut(BaseUser):
    is_admin: bool


class UserIn(UserOut):
    password: str


class UsersOut(BaseModel):
    __root__: List[UserOut]












