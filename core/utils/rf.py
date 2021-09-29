import os
from typing import List

from sqlmodel import Session
from pydantic import parse_obj_as
import requests

from core.models.products_rf import ProductRF, ProductRFBase, SchemaProductRF
from core.db.database import engine
from core.crud.rf_product import CRUDRF

crud = CRUDRF(ProductRF)


class RF:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL_RF')

    def create_rf_product(self, session: Session = Session(engine)):
        products = self.crawl_rf_products()
        crud.list_create(parse_obj_as(List[SchemaProductRF], products), session)

    def last_page(self) -> int:
        return int(requests.get(self.base_url).json()['meta']['last_page'])

    def crawl_rf_products(self) -> list:
        total_page = self.last_page()
        products = []
        for page in range(total_page):
            data = requests.get(self.base_url + f'?page={page}').json()['data']
            for product in data:
                products.append(product)

        return products