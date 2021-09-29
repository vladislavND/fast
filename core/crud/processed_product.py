import datetime
import typing

import pandas as pd
from sqlmodel import Session, select

from core.crud.base import ModelType, CRUDBase
from core.crud.product import CRUDProduct
from core.crud.rf_product import CRUDRF
from core.models.product import Product
from core.models.products_rf import ProductRF
from core.models.processed_product import ProcessedProduct


class CRUDProcessed(CRUDBase):

    def add_processed_products(self, session: Session, file: typing.ByteString, shop_id: int):
        crud_rf = CRUDRF(ProductRF)
        crud_product = CRUDProduct(Product)
        file = pd.read_excel(file)
        df = file.fillna(0)
        articles_product = [i for i in df[df.columns[5]]]
        articles_rf = [i for i in df[df.columns[0]]]
        index = -1
        for article in articles_product:
            index += 1
            product = crud_product.get_by_article(
                session=session,
                article=article,
                shop_id=shop_id
            )
            product_rf = crud_rf.get_product_rf_by_article(
                session=session,
                article=articles_rf[index]
            )
            if product and product_rf:
                processed_product = ProcessedProduct(
                    price=product.price, price_rf=product_rf.price,
                    sale_price=product.sale_price, article=str(product.article),
                    article_rf=product_rf.article, shop_id=shop_id,
                    date=datetime.datetime.now()
                )
                session.add(processed_product)
        session.commit()




