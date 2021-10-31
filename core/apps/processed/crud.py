import datetime
import typing

import pandas as pd
from sqlmodel import Session, select

from core.apps.crud_base import CRUDBase
from core.apps.products.crud import CRUDProduct
from core.apps.products.models import Product
from core.apps.processed.models import ProcessedProduct


class CRUDProcessed(CRUDBase):

    def get_by_shop_id(self, session: Session, shop_id: int) -> typing.List[ProcessedProduct]:
        statement = select(self.model).where(self.model.shop_id == shop_id)
        products = session.exec(statement).all()
        return products

    def add_processed_products(self, session: Session, file: typing.ByteString, shop_id: int):
        crud_product = CRUDProduct(Product)
        file = pd.read_excel(file)
        df = file.fillna(0)
        articles_product = [i for i in df[df.columns[5]]]
        articles_rf = [i for i in df[df.columns[0]]]
        price_rf_kg = [i for i in df[df.columns[4]]]
        price_rf = [i for i in df[df.columns[3]]]
        index = -1
        for article in articles_product:
            index += 1
            product = crud_product.get_by_article(
                session=session,
                article=article,
                shop_id=shop_id
            )
            if product:
                processed_product = ProcessedProduct(
                    price=product.price, price_rf=price_rf[index],
                    sale_price=product.sale_price, article=str(product.article),
                    article_rf=articles_rf[index], shop_id=shop_id,
                    date=datetime.datetime.now(),  price_rf_kg=price_rf_kg[index],
                    name=product.name, weight=product.weight, unit=product.unit
                )
                session.add(processed_product)
        session.commit()




