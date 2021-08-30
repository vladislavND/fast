from datetime import date

from sqlalchemy import Column, String, DECIMAL, Date, BigInteger

from core.db.database import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(BigInteger, primary_key=True)
    url = Column(String)
    shop = Column(String)
    name = Column(String)
    article = Column(String)
    price = Column(DECIMAL)
    sale_price = Column(DECIMAL, nullable=True)
    different_price = Column(DECIMAL, nullable=True)
    date = Column(Date, autoincrement=True, default=date.today())
