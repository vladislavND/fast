from typing import List
import io

from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import StreamingResponse

from core.apps.products.schema import DirectoryFolders
from core.db.dependecy import get_db
from core.apps.products.crud import CRUDProduct
from core.apps.products.models import ProductBase, Product
from core.utils.manager import Manager

router = APIRouter()
crud = CRUDProduct(Product)


@router.get('/products', response_model=List[Product])
def get_products(session: Session = Depends(get_db)):
    products = crud.get_all(session)

    return products


@router.get('/product/{product_id}', response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_db)):
    product = crud.get(product_id, session=session)
    return product


@router.post('/product')
def create_product(product: ProductBase, session: Session = Depends(get_db)):
    return crud.create(product, session)


@router.post('/products', status_code=status.HTTP_201_CREATED)
def create_products(products: List[ProductBase], session: Session = Depends(get_db)):
    crud.list_create(products, session)
    return 'Successfully created products'


@router.post('/all_xlsx', response_class=StreamingResponse)
def get_all_products(data: DirectoryFolders):
    df = Manager(shop_id=data.shop_id, file_name=data.file_name).open()
    to_write = io.BytesIO()
    df.to_excel(to_write, index=False)
    to_write.seek(0)
    return StreamingResponse(to_write, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
