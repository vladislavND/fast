
from typing import List

from sqlmodel import Session, select


from core.apps.crud_base import CRUDBase
from core.apps.price.models import Price


class CRUDPrice(CRUDBase):

    def get_price_by_article(self, session: Session, article: int) -> List[Price]:
        price = session.exec(select(self.model).filter_by(article=article)).all()
        return price
