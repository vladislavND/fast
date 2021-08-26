from sqlalchemy.orm import Session

from core.models import product as model
from core.schemas import product as schema


def get_product(db: Session, product_id: int):
    return db.query(model.Product).filter(model.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schema.ProductBase):
    print(product)
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

