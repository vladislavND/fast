from sqlmodel import Session, select

from core.apps.crud_base import CRUDBase
from core.apps.products.models import Product


class CRUDProduct(CRUDBase):

    def get_by_article(self, session: Session, article: int, shop_id: int) -> Product:
        statement = select(self.model).where(self.model.article == str(article), self.model.shop_id == shop_id)
        query = session.exec(statement).first()
        if query:
            return query

