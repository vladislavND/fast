from fastapi import FastAPI, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.db.dependecy import get_db
from core.routs import product, shop, processed_products, user, scrapyd, price
from core.db.database import Base, engine, SessionLocal
from core.crud.shop import create_shops
from core.schemas.shop import ShopList

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(product.router, prefix="/api", tags=["Product"])
app.include_router(processed_products.router, prefix="/api", tags=["ProcessedProduct"])
app.include_router(shop.router, prefix="/api", tags=["Shop"])
app.include_router(user.router, prefix="/api", tags=["User"])
app.include_router(scrapyd.router, prefix='/api', tags=["Scrapyd"])
app.include_router(price.router, prefix='/api', tags=["Price"])


@app.on_event('startup')
def create_category():
    shops = [
        {'name': 'Utkonos', 'url': 'https://utkonos.ru', 'id': 3},
        {'name': 'Ecomarket', 'url': 'https://ecomarket.ru', 'id': 2},
        {'name': 'Фундучок', 'url': 'https://фундучок.рф', 'id': 1},
        {'name': 'Vkusvill', 'url': 'https://vkusvill.ru', 'id': 4}
    ]
    db: Session = SessionLocal()
    try:
        create_shops(db, ShopList.parse_obj(shops))
    except IntegrityError:
        pass








