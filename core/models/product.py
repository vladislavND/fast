from datetime import date

from sqlalchemy import Column, Boolean, String, Integer, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship

from core.db.database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(DECIMAL)
    sale_price = Column(DECIMAL, nullable=True)
    description = Column(String, nullable=True)
    weight = Column(Integer, nullable=True)
    unit = Column(String, nullable=True)
    sale = Column(Integer, nullable=True)
    tags = Column(String, nullable=True)
    attributes = Column(String, nullable=True)
    chars = Column(String, nullable=True)
    available = Column(Boolean, nullable=True)
    available_count = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    date = Column(Date, autoincrement=date)
    shop_id = Column(Integer, ForeignKey('shop.id'))
    shop = relationship('Shop', back_populates="products")






















