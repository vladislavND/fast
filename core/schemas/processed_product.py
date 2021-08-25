from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from core.schemas.product import ProductBase


class ProcessedProduct(ProductBase):
    price_rf: Optional[Decimal] = None
    price_rf_kg: Optional[Decimal] = None
    price_kg: Optional[Decimal] = None
    different_price: Optional[int] = None


class ProductProcessedOut(ProcessedProduct):
    id: int


class ProcessedProductsList(BaseModel):
    __root__: List[ProcessedProduct]


class ProcessedProductListOut(BaseModel):
    __root__: List[ProductProcessedOut]

