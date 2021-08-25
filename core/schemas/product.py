from decimal import Decimal
from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: Decimal
    sale_price: Optional[Decimal] = None
    description: Optional[str] = None
    weight: Optional[int] = None
    unit: Optional[str] = None
    sale: Optional[int] = None
    tags: Optional[str] = None
    attributes: Optional[str] = None
    chars: Optional[str] = None
    available: Optional[bool] = None
    available_count: Optional[int] = None
    url: Optional[str] = None
    date: date
    shop_id: int

    class Config:
        orm_mode = True


class ProductOut(ProductBase):
    id: int


class ProductList(BaseModel):
    __root__: List[ProductBase]


class ProductListOut(BaseModel):
    __root__: List[ProductOut]











