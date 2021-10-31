from typing import Any, List

from sqlmodel import Session, select

from core.apps.crud_base import CRUDBase
from core.apps.shop.models import Shop, File, FileBase


class CRUDShop(CRUDBase):

    def get_by_name(self, session: Session, name: str) -> Shop:
        statement = select(self.model).where(self.model.name == name.title())
        shop = session.exec(statement).one_or_none()
        return shop

    def create_path_file(self, session: Session, data: FileBase, model: File) -> Shop:
        files = model.from_orm(data)
        session.add(files)
        session.commit()
        return files

    def get_all_files_by_shop_id(self, session: Session, shop_id: int, model: File) -> List[File]:
        statement = select(model).where(model.shop_id == shop_id)
        files = session.exec(statement).all()
        return files




