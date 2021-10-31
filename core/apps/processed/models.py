import datetime
from typing import Optional, List
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship
from pydantic import root_validator

from core.apps.shop.models import Shop


class ProcessedProductBase(SQLModel):
    price: Decimal
    price_kg: Optional[Decimal] = None
    price_rf_kg: Optional[Decimal] = None
    price_rf: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    different_price: Optional[Decimal] = None
    name: str
    date: datetime.date = datetime.date.today()
    article: str
    article_rf: str
    weight: Optional[str] = None
    unit: Optional[str] = None

    shop_id: Optional[int] = Field(default=None, foreign_key='shop.id')
    shop: List[Shop] = Relationship(back_populates="processed_products")

    @root_validator
    def price_to_kg(cls, values):
        if values['unit'] in ['г', 'кг']:
            if values['sale_price']:
                price_kg = Decimal(values['sale_price']) / Decimal(values['weight'])
                values['price_kg'] = price_kg
                return values
            price_kg = Decimal(values['price']) / Decimal(values['weight'])
            values['price_kg'] = price_kg
        return values

    @root_validator
    def calc_difference(cls, values):
        if values['price_kg']:
            values['different_price'] = values['price_kg'] - values['price_rf_kg']
        values['different_price'] = values.get('price') - values.get('price_rf')

        return values


class ProcessedProduct(ProcessedProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)