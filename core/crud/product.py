import io

from sqlalchemy.orm import Session
import pandas as pd
from starlette.responses import StreamingResponse

from core.models import product as model
from core.schemas import product as schema


def get_product(db: Session, product_id: int):
    return db.query(model.Product).filter(model.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schema.ProductBase):
    db_product = model.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_products(db: Session, products: schema.ProductList):
    for product in products.__root__:
        db_products = model.Product(**product.dict())
        db.add(db_products)
        db.commit()
        db.refresh(db_products)
    return


def get_all_products(db: Session):
    all_products = db.query(model.Product)
    sql = pd.read_sql(all_products.statement, db.bind)
    sql.to_excel('products.xlsx', sheet_name='Sheet1')
    return sql


def get_all_products_by_shop_id(db: Session, shop_id: int):
    all_products = db.query(model.Product).filter(model.Product.shop_id == shop_id)
    sql = pd.read_sql(all_products.statement, db.bind)
    sql.to_excel(f'{shop_id}_products.xlsx', sheet_name='Sheet1')
    return sql
