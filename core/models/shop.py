from sqlalchemy import Column, String, Integer

from core.db.database import Base
from sqlalchemy.orm import relationship


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String)

    products = relationship("Product", back_populates="shop")
    processed_products = relationship("ProcessedProduct", back_populates="shop")

