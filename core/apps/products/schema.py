from decimal import Decimal
from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: Decimal
    sale_price: Optional[Decimal] = None
    article: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[str] = None
    unit: Optional[str] = None
    sale: Optional[int] = None
    tags: Optional[str] = None
    attributes: Optional[str] = None
    chars: Optional[str] = None
    available: Optional[bool] = None
    available_count: Optional[int] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    date: date = None
    shop_id: int

    class Config:
        orm_mode = True


class ProductOut(ProductBase):
    id: int


class ProductList(BaseModel):
    __root__: List[ProductBase]


class ProductListOut(BaseModel):
    __root__: List[ProductOut]


class DirectoryFolders(BaseModel):
    file_name: str
    shop_id: int






