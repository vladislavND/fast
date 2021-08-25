from sqlalchemy import Column, String, Integer

from core.db.database import Base


class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    url = Column(String, unique=True)


