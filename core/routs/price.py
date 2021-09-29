from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.db.dependecy import get_db
from core.models.price import PriceBase, Price, PriceIn
from core.crud.price import CRUDPrice
from core.utils.price_parser import PriceShopParser

router = APIRouter()
crud = CRUDPrice(model=Price)


@router.post('/price', response_model=PriceBase)
def get_price(data: PriceIn, session: Session = Depends(get_db)):
    data = PriceShopParser().compare(url=data.url, product_id=data.rf_article)
    data = PriceBase(**data)
    return crud.create(data, session)


@router.get('/price/{article}', response_model=List[Price])
def get_prices(article, session: Session = Depends(get_db)):
    data = crud.get_price_by_article(session, article)
    return data
