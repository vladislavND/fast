from sqlalchemy.orm import Session

from core.models import user as model
from core.schemas import user as schema
from utils.security import get_password_hash


def get_user(db: Session, telegram_id: int):
    return db.query(model.User).filter(model.User.telegram_id == telegram_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(model.User).offset(skip).limit(limit).all()
    return users


def create_user(db: Session, user: schema.UserIn):
    user.password = get_password_hash(user.password)
    db_user = model.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return


