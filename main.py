from fastapi import FastAPI
from core.routs import product, shop, processed_products, user, scrapyd, price
from core.db.database import Base, engine

Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(product.router, prefix="/api", tags=["Product"])
app.include_router(processed_products.router, prefix="/api", tags=["ProcessedProduct"])
app.include_router(shop.router, prefix="/api", tags=["Shop"])
app.include_router(user.router, prefix="/api", tags=["User"])
app.include_router(scrapyd.router, prefix='/api', tags=["Scrapyd"])
app.include_router(price.router, prefix='/api', tags=["Price"])









