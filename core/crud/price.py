
from typing import List

from sqlmodel import Session, select


from core.crud.base import CRUDBase, ModelType


class CRUDPrice(CRUDBase):

    def get_price_by_article(self, session: Session, article: int) -> List[ModelType]:
        price = session.exec(select(self.model).filter_by(article=article)).all()
        return price
