from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.db.dependecy import get_db
from core.apps.shop.crud import CRUDShop
from core.apps.shop.models import Shop, ShopBase, FileBase, File

router = APIRouter()
crud = CRUDShop(Shop)


@router.get('/shops', response_model=List[Shop])
def get_shops(session: Session = Depends(get_db)):
    return crud.get_all(session)


@router.get('/shop/{shop_id}', response_model=Shop)
def get_shop(shop_id: int,  session: Session = Depends(get_db)):
    return crud.get(shop_id, session)


@router.post('/shop', response_model=Shop)
def create_shop(shop: ShopBase,  session: Session = Depends(get_db)):
    return crud.create(shop, session)


@router.post('/shops')
def create_shops(shops: List[ShopBase],  session: Session = Depends(get_db)):
    return crud.list_create(shops, session)


@router.post('/add_file_shop', response_model=File)
def add_file_shop(files: FileBase, session: Session = Depends(get_db)):
    return crud.create_path_file(session=session, data=files, model=File)


@router.post('/get_files_by_shop_id', response_model=List[File])
def get_file_by_shop_id(shop_id: int, session: Session = Depends(get_db)):
    return crud.get_all_files_by_shop_id(session=session, shop_id=shop_id, model=File)




