from asyncio import run


from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from pydantic import parse_obj_as
from typing import List

from core.routs.product import router as product_router
from core.routs.shop import router as shop_router
from core.routs.price import router as price_router
from core.routs.user import router as user_router
from core.routs.scrapyd import router as scrapyd_router
from core.routs.processed_products import router as processed_products_router

from core.models.shop import Shop
from core.models.product import Product
from core.models.products_rf import ProductRF
from core.models.processed_product import ProcessedProduct
from core.models.price import Price


from core.crud.shop import CRUDShop
from core.db.database import engine
from sqlalchemy.exc import IntegrityError
from front_bot.loader import dp, executor, bot


app = FastAPI()
app.include_router(product_router, prefix="/api", tags=["Product"])
app.include_router(processed_products_router, prefix="/api", tags=["ProcessedProduct"])
app.include_router(shop_router, prefix="/api", tags=["Shop"])
app.include_router(user_router, prefix="/api", tags=["User"])
app.include_router(scrapyd_router, prefix='/api', tags=["Scrapyd"])
app.include_router(price_router, prefix='/api', tags=["Price"])


@app.on_event('startup')
async def create_category(session: Session = Session(engine)):

    SQLModel.metadata.create_all(engine)
    try:
        shops = [
            {'name': 'Utkonos', 'url': 'https://utkonos.ru', 'id': 3},
            {'name': 'Ecomarket', 'url': 'https://ecomarket.ru', 'id': 2},
            {'name': 'Фундучок', 'url': 'https://фундучок.рф', 'id': 1},
            {'name': 'Vkusvill', 'url': 'https://vkusvill.ru', 'id': 4},
            {'name': 'Wildbress', 'url': 'https://vkusvill.ru', 'id': 5},
        ]
        CRUDShop(Shop).list_create(session=session, objects=parse_obj_as(List[Shop], shops))
    except IntegrityError:
        pass









