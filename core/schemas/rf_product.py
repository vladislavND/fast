from decimal import Decimal

from pydantic import BaseModel, Field


class SchemaProductRF(BaseModel):
    article: int = Field(alias='id')
    name: str
    price: Decimal


class SchemaProductRFOut(BaseModel):
    id: int
    article: int
    name: str
    price: Decimal

    class Config:
        orm_mode = True