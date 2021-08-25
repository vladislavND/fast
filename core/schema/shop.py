from typing import List

from pydantic import BaseModel


class Shop(BaseModel):
    name: str
    url: str


class ShopOut(Shop):
    id: int


class ShopList(BaseModel):
    __root__: List[ShopOut]
