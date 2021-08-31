import json
import time

import scrapy
from scrapy.http import JsonRequest
import requests

from parsing.methods import telegram_info
from parsing.request import send_products


class EcomarketSpider(scrapy.Spider):
    name = 'ecomarket'
    allowed_domains = ['api.ecomarket.ru',]
    category = []
    articles = []
    products = []

    def start_requests(self):
        data = {"action":"appStartUp_v3","REGION":"77","AB_CASE":"A","token":"9a32530d9947fdfc546cb2931d6a750e"}
        yield JsonRequest('https://api.ecomarket.ru/api.php', callback=self.parse, data=data)

    def get_categories(self, groups: list, **kwargs):
        categories = []
        for cats in self.category:
            for group in groups:
                if group in cats:
                    categories.append(cats[group])
                if group in cats['children']:
                    categories.append(cats['children'][group])
        return ' | '.join(categories)

    def parse(self, response, **kwargs):
        response_json = json.loads(response.text)
        data_products = response_json.get('data').get('products')
        data_category = response_json.get('data').get('groups')
        for categories in data_category:
            for children in categories['children']:
                self.category.append({categories['id']: categories['title'],
                                      'children': {children['id']: children['title']}})
        urls = [value['url'] for _, value in data_products.items()]
        for url in urls:
            try:
                data = {"action": "getProductByUrl_v2", "url": url, "region": "77", "token": "fb45d09e58d75f295f2004c4fa53e966"}
                response_data = requests.post('https://api.ecomarket.ru/api.php', data=data).json().get('data')
                groups = response_data['all_groups']
                self.articles.append(response_data['id'])
            except:
                time.sleep(5)

            product = {
                'attributes': f"Белки: {response_data['bel_amount']}",
                'image_url': response_data['big'],
                'unit': response_data['ed_izm'],
                'category': self.get_categories(groups),
                'article': response_data['id'],
                'sale_price': response_data['old_price'],
                'price': response_data['price'],
                'name': response_data['title'],
                'url': response_data['url'],
                'weight': response_data['peramount'],
                'shop_id': 2
            }
            self.products.append(product)

            yield product

    def close(self, reason):
        send_products(self.products)
        telegram_info(self.name)



















