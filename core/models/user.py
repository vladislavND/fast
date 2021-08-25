from sqlalchemy import Column, String, Integer, Boolean, BigInteger

from core.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    telegram_id = Column(BigInteger, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)









