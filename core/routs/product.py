from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from core.schemas import product
from core.db.dependecy import get_db
from core.crud import product as crud

router = APIRouter()


@router.get('/products', response_model=product.ProductListOut)
def get_products(db: Session = Depends(get_db)):

    return crud.get_products(db)


@router.get('/product/{product_id}', response_model=product.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.post('/product')
def create_product(item: product.ProductBase, db: Session = Depends(get_db)):
    crud.create_product(db, item)
    return item


@router.post('/products', status_code=status.HTTP_201_CREATED)
def create_products(products: product.ProductList, db: Session = Depends(get_db)):
    crud.create_products(db, products)
    return 'Successfully created products'


@router.post('/all_xlsx', response_class=StreamingResponse)
def get_all_xlsx(db: Session = Depends(get_db)):
    crud.get_all_products(db)
    file = open('test.xlsx', mode='rb')
    return StreamingResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@router.post('/all_xlsx/{shop_id}', response_class=StreamingResponse)
def get_all_products(shop_id: int, db: Session = Depends(get_db)):
    crud.get_all_products_by_shop_id(db, shop_id)
    file = open(f'{shop_id}_products.xlsx', mode='rb')
    return StreamingResponse(file, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
