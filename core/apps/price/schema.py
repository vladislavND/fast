from datetime import date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


class PriceBase(BaseModel):
    url: str
    shop: str
    article: str
    name: str
    price: Decimal
    sale_price: Optional[Decimal] = None
    different_price: Optional[Decimal] = None
    date: date

    class Config:
        orm_mode = True


class PriceOut(PriceBase):
    id: int


class PriceIn(BaseModel):
    rf_article: Optional[str]
    url: str


class ListPrice(BaseModel):
    __root__: List[PriceOut]



