import os

import requests
from requests import request

BASE_URL = os.getenv('BASE_URL')


class Request:

    def get_price(self, url) -> str:
        rs = request(url=BASE_URL+'/api/price', method='POST', json={'url': url})
        text = self.format_dict_to_string(rs.json())
        return text

    def get_all_price(self, article: str) -> str:
        rs = request(url=BASE_URL+f'/api/price/{article}', method='GET')
        text = self.format_dict_to_string(rs.json())
        return text

    def format_dict_to_string(self, data: dict) -> str:
        msg = f"Наименование: {data.get('name')}\nЦена: {data.get('price')}\nМагазин: {data.get('shop')}\n" \
              f"Артикул: {data.get('article')}\nUrl: {data.get('url')}\nЦена со скидкой: {data.get('sale_price')}\n" \
              f"Разница в цене: {data.get('different_price')}"
        return msg

    def get_spiders(self) -> list:
        data = request(method='GET', url=BASE_URL+'/api/scrapyd/parsing')
        return ['□ ' + spider for spider in data.json()]

    @classmethod
    def start_spider(cls, spiders: list):
        for spider in spiders:
            data = {'spider': spider}
            request(method='POST', url=BASE_URL+'/api/scrapyd/run', json=data)


class Product:

    @classmethod
    def get_xlsx_products(cls):
        rs = requests.post(url=BASE_URL+'/api/all_xlsx')
        return rs.content

    @classmethod
    def get_files_folder(cls, shop_name):
        rs = requests.post(
            url=BASE_URL+f'/api/get_files/{shop_name}'
        )

        return rs.json()

    @classmethod
    def get_products_by_shop_id(cls, shop_name='wildbress'):
        rs = requests.post(url=BASE_URL+f'/api/all_xlsx/{shop_name}')
        return rs.content

    @classmethod
    def get_shops(cls):
        rs = requests.get(url=BASE_URL+'/api/shops')
        return rs.json()

    @classmethod
    def send_processing_product(cls, shop_id, file):
        requests.post(
            url=BASE_URL + f'/api/processed_product_xlsx/{shop_id}',
            files={'file': ('report.xls', file, 'application/vnd.ms-excel',)}
        )








