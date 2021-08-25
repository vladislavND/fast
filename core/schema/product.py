from decimal import Decimal
from datetime import date
from typing import List

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: Decimal
    sale_price: Decimal = None
    description: str = None
    weight: int = None
    unit: str = None
    sale: int = None
    tags: str = None
    attributes: str = None
    chars: str = None
    available: bool = None
    available_count: int = None
    url: str = None
    date: date
    shop_id: int

    class Config:
        orm_mode = True


class FilterProduct(ProductBase):
    price_rf: Decimal = None
    price_rf_kg: Decimal = None
    price_kg: Decimal = None
    different_price: int = None


class ProductOut(ProductBase):
    id: int
    shop: str


class ProductFilterOut(FilterProduct):
    id: int
    shop: str


class ProductList(BaseModel):
    __root__: List[ProductBase]


class FilterProductsList(BaseModel):
    __root__: List[FilterProduct]


class ProductListOut(BaseModel):
    __root__: List[ProductOut]


class FilterProductListOut(BaseModel):
    __root__: List[ProductFilterOut]









