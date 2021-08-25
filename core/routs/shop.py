from fastapi import APIRouter

from core.schema.shop import Shop, ShopOut, ShopList

router = APIRouter()


@router.get('/shop', response_model=ShopList)
def get_all_shops():
    pass


@router.get('/shop/{id}', response_model=ShopOut)
def get_shop(id: int):
    pass


@router.post('/shop')
def create_product(product: Shop):
    pass

