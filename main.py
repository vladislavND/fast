from fastapi import FastAPI
from core.routs import products, shop
from core.db.database import Base, engine

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(products.router, prefix="/api", tags=["products"])
app.include_router(shop.router, prefix="/api", tags=["shops"])









