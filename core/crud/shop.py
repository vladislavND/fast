from sqlalchemy.orm import Session

from core.models import shop as model
from core.schemas import shop as schema


def get_shop(db: Session, shop_id: int):
    return db.query(model.Shop).filter(model.Shop.id == shop_id).first()


def get_shops(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Shop).offset(skip).limit(limit).all()


def create_shop(db: Session, shop: schema.Shop):
    db_product = model.Shop(**shop.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_shops(db: Session, shops: schema.ShopList):
    for shop in shops.__root__:
        db_products = model.Shop(**shop.dict())
        db.add(db_products)
        db.commit()
        db.refresh(db_products)
    return

