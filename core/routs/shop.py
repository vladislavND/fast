from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.schemas.shop import Shop, ShopOut, ShopList
from core.db.dependecy import get_db
from core.crud import shop as crud

router = APIRouter()


@router.get('/shops', response_model=ShopList)
def get_shops(db: Session = Depends(get_db)):
    shops = crud.get_shops(db)
    return shops


@router.get('/shop/{shop_id}', response_model=ShopOut)
def get_shop(shop_id: int,  db: Session = Depends(get_db)):
    shop = crud.get_shops(db, shop_id)
    return shop


@router.post('/shop', response_model=ShopOut)
def create_shop(shop: Shop,  db: Session = Depends(get_db)):
    item = crud.create_shop(db, shop)
    return item


@router.post('/shops')
def create_shops(shops: ShopList,  db: Session = Depends(get_db)):
    crud.create_shops(db, shops)
