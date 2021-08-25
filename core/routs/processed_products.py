from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.schemas import processed_product
from core.db.dependecy import get_db
from core.crud import processed_product as crud

router = APIRouter()


@router.get('/processed_products', response_model=processed_product.ProcessedProductListOut)
def get_processed_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@router.get('/processed_product/{product_id}', response_model=processed_product.ProcessedProduct)
def get_processed_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)





