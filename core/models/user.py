from typing import Optional

from sqlmodel import SQLModel,  Field


class UserBase(SQLModel):
    username: str
    telegram_id: int
    password: str
    is_admin: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)










