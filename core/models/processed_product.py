import datetime
from typing import Optional, List
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship

from core.models.shop import Shop


class ProcessedProductBase(SQLModel):
    price: Decimal
    price_rf: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    date: datetime.date = datetime.date.today()
    article: str
    article_rf: str
    shop_id: Optional[int] = Field(default=None, foreign_key='shop.id')
    shop: List[Shop] = Relationship(back_populates="processed_products")


class ProcessedProduct(ProcessedProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)