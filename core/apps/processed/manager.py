import pandas as pd
from sqlmodel import Session
from core.db.database import engine

from core.apps.processed.crud import CRUDProcessed
from core.apps.processed.models import ProcessedProduct


class AnaliseProducts:
    def __init__(self):
        self.processed = CRUDProcessed(ProcessedProduct)

    def price_difference(self):
        price, sale_price, price_rf, different_price, \
        article, article_rf, shop_id, name, weight, price_rf_kg, price_kg = [], [], [], [], [], [], [], [], [], [], []
        products = self.processed.get_all(Session(engine))
        mapping = {
            2: 'Ecomarket',
            3: 'Utkonos',
            4: 'Vkusvill',
            5: 'Wildbress',
            1: 'Funduchok',
            6: 'Riboedov'
        }
        for product in products:
            price.append(product.price)
            sale_price.append(product.sale_price)
            different_price.append(product.different_price)
            price_rf.append(product.price_rf)
            article.append(product.article)
            article_rf.append(product.article_rf)
            shop_id.append(mapping[product.shop_id])
            name.append(product.name)
            weight.append(product.weight)
            price_rf_kg.append(product.price_rf_kg)
            price_kg.append(product.price_kg)
        headers = ['Цена магазина', 'Цена со скидкой', 'Цена РФ', 'Разница в цене',
                   'Артикул', 'Артикул рф', 'Магазин', 'Наименование', 'Вес', 'Цена за кг РФ', 'Цена за кг']
        df = pd.DataFrame(
            list(
                zip(
                    price, sale_price, price_rf, different_price, article,
                    article_rf, shop_id, name, weight, price_rf_kg, price_kg
                    )
            ), columns=headers
        )

        return df


