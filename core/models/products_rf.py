from typing import Optional
from decimal import Decimal

from sqlmodel import SQLModel, Field
from pydantic import Field as f, BaseModel


class ProductRFBase(SQLModel):
    name: Optional[str] = None
    article: Optional[str] = None
    price: Optional[Decimal] = None


class ProductRF(ProductRFBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class SchemaProductRF(BaseModel):
    name: Optional[str] = None
    article: Optional[str] = f(alias='id')
    price: Optional[Decimal] = None