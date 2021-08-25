from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
def create_product(product: product.ProductBase, db: Session = Depends(get_db)):
    item = crud.create_product(db, product)
    return item


@router.post('/products', status_code=status.HTTP_201_CREATED)
def create_products(products: product.ProductList, db: Session = Depends(get_db)):
    crud.create_products(db, products)
    return 'Successfully created products'



