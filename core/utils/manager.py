import json
from typing import List

import pandas as pd
from pydantic import parse_obj_as
from sqlmodel import Session

from core.db.database import engine
from core.apps.products.models import Product, ProductBase
from core.apps.shop.models import Shop, File
from core.apps.products.crud import CRUDProduct
from core.apps.shop.crud import CRUDShop


class Manager:
    def __init__(self, shop_id: int, file_name: str = None):
        self.shop_id = shop_id
        self.file_name = file_name

    def open(self) -> pd.DataFrame:
        crud = CRUDShop(Shop).get_all_files_by_shop_id(shop_id=self.shop_id, session=Session(engine), model=File)[0]
        df = pd.read_csv(
            f'{crud.path}/{self.file_name}',
            sep=';', encoding='utf-8', low_memory=False, index_col=False
        )
        return df

    def find_by_article(self, article: int) -> pd.DataFrame:
        df = self.open()
        result = df.loc[df['article'] == article]
        return result

    def create(self, session: Session = Session(engine)):
        df = self.open()
        df['shop_id'] = self.shop_id
        df1 = df[['article', 'price', 'sale_price', 'shop_id', 'weight', 'unit', 'name']]
        json_data = df1.to_json(index=False, orient='table')
        data = json.loads(json_data)['data']
        objects = parse_obj_as(List[ProductBase], data)
        CRUDProduct(Product).list_create(session=session, objects=objects)

























