from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.schemas import price
from core.db.dependecy import get_db
from core.crud import price as crud

router = APIRouter()


@router.post('/price', response_model=price.PriceBase)
def get_price(data: price.PriceIn, db: Session = Depends(get_db)):
    data = crud.PriceShopParser().compare(url=data.url, product_id=data.rf_article)
    crud.create_price(db, data)
    return crud.create_price(db, data)


@router.get('/price/{article}', response_model=price.ListPrice)
def get_prices(article, db: Session = Depends(get_db)):
    data = crud.get_price_by_article(db, article)
    return data
