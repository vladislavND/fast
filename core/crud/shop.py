from sqlmodel import Session, select

from core.crud.base import CRUDBase, ModelType
from core.models.shop import Shop


class CRUDShop(CRUDBase):

    def get_by_name(self, session: Session, name: str) -> Shop:
        statement = select(self.model).where(self.model.name == name.title())
        shop = session.exec(statement).one_or_none()
        return shop


