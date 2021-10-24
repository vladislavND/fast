from sqlmodel import Session, select

from core.crud.base import CRUDBase
from core.models.products_rf import ProductRF


class CRUDRF(CRUDBase):

    def get_product_rf_by_article(self, session: Session, article: str) -> ProductRF:
        statement = select(self.model).where(
            self.model.article == article,
        )
        query = session.exec(statement).first()
        if query:
            return query


