from fastapi import APIRouter

from core.schema import product

router = APIRouter()


@router.get('/products', response_model=product.ProductListOut)
def get_all_products(products: product.ProductListOut):
    return products


@router.get('/product/{id}', response_model=product.ProductOut)
def get_product(id: int):
    pass


@router.post('/product')
def create_product(product: product.ProductBase):
    pass


@router.post('/products')
def create_products(products: product.ProductList):
    pass



