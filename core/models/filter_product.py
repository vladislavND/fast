from sqlalchemy import Column, Boolean, String, Integer, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship

from core.db.database import Base


class FilterProduct(Base):
    __tablename__ = 'filter_products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(DECIMAL)
    price_rf = Column(DECIMAL, nullable=True)
    price_rf_kg = Column(DECIMAL, nullable=True)
    price_kg = Column(DECIMAL, nullable=True)
    sale_price = Column(DECIMAL, nullable=True)
    description = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    sale = Column(Integer, nullable=True)
    tags = Column(String, nullable=True)
    attributes = Column(String, nullable=True)
    chars = Column(String, nullable=True)
    different_price = Column(Integer, nullable=True)
    available = Column(Boolean, nullable=True)
    available_count = Column(Integer, nullable=True)
    date = Column(Date)
    shop_id = Column(Integer, ForeignKey('shops.id'))
    shop = relationship('Shop', back_populates="filter_products")