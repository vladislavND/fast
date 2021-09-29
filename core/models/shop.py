from typing import List, Optional

from sqlmodel import SQLModel, Relationship, Field


class ShopBase(SQLModel):
    name: str
    url: str

    products: List["Product"] = Relationship(back_populates="shop")
    processed_products: List["ProcessedProduct"] = Relationship(back_populates="shop")


class Shop(ShopBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


