import json
import re
from datetime import date
from typing import List
import os

import pandas as pd
from pydantic import parse_obj_as
from sqlmodel import Session

from core.db.database import engine
from core.models.product import Product, ProductBase
from core.models.processed_product import ProcessedProduct
from core.models.shop import Shop
from core.crud.product import CRUDProduct
from core.crud.processed_product import CRUDProcessed
from core.crud.shop import CRUDShop


class Manager:
    def __init__(self, shop_name: str, file_name: str =None):
        self.shop_name = shop_name.lower()
        self.file_name = file_name

    def get_files_folders(self):
        data = {}
        files = os.listdir(f'parse_files/{self.shop_name}')
        for file in files:
            data.update({file: file})
        return data

    def open(self) -> pd.DataFrame:
        directory_name = re.sub(r'[^A-Za-z]', '', self.shop_name).replace('csv', '')
        df = pd.read_csv(
            f'parse_files/{directory_name}/{self.shop_name}',
            sep=';', encoding='utf-8', low_memory=False, index_col=False
        )
        return df

    def find_by_article(self, article: int) -> pd.DataFrame:
        df = self.open()
        result = df.loc[df['article'] == article]
        return result

    def create(self, shop_id: int, session: Session = Session(engine)):
        df = self.open()
        df['shop_id'] = shop_id
        df1 = df[['article', 'price', 'sale_price', 'shop_id']]
        json_data = df1.to_json(index=False, orient='table')
        data = json.loads(json_data)['data']
        objects = parse_obj_as(List[ProductBase], data)
        CRUDProduct(Product).list_create(session=session, objects=objects)

    def analize(self, session: Session = Session(engine)):
        processed_crud = CRUDProcessed(ProcessedProduct)
        shop_crud = CRUDShop(Shop)
        shop_id = shop_crud.get_by_name(session, self.shop_name).id
        processed_products = processed_crud.get_by_shop_id(session, shop_id)

        # TODO: Доделать аналитику

























