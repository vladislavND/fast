from fastapi import HTTPException
from sqlmodel import Session, select

from core.crud.base import CRUDBase
from core.models.user import User
from core.utils.security import get_password_hash


class CRUDUser(CRUDBase):
    def create_user(self, session: Session, user: User) -> User:
        user.password = get_password_hash(user.password)
        to_object = self.model.from_orm(user)
        session.add(to_object)
        session.commit()
        session.refresh(to_object)
        return to_object

    def get_by_telegram_id(self, session: Session, telegram_id: int) -> User:
        user = session.exec(select(self.model).filter_by(telegram_id=telegram_id)).one()
        if not user:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} by telegram_id {telegram_id} not found")
        return user







