from sqlalchemy.orm import Session

from core.models import processed_product as model


def get_product(db: Session, product_id: int):
    return db.query(model.ProcessedProduct).filter(model.ProcessedProduct.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.ProcessedProduct).offset(skip).limit(limit).all()


