from sqlmodel import Session, select

from core.crud.base import CRUDBase, ModelType


class CRUDRF(CRUDBase):

    def get_product_rf_by_article(self, session: Session, article: str) -> ModelType:
        statement = select(self.model).where(self.model.article == str(article))
        query = session.exec(statement).first()
        if query:
            return query


