from decimal import Decimal
import re

from requests import request
from bs4 import BeautifulSoup

rf_url = "https://api.rf.market/api/integration/products?page=1"
rf_url_format = "https://api.rf.market/api/integration/products/{prod_id}"


class PriceShopParser:

    def price_rf(self, prod_id):
        rs = request(url=rf_url_format.format(prod_id=prod_id), method='GET')
        price = rs.json()['data']['price']
        return price

    def price_ecomarket(self, url: str):
        api = 'https://api.ecomarket.ru/api.php'
        format_url = url.replace('https://ecomarket.ru/', '')
        json = {
            "action": "getProductByUrl_v2",
            "url": format_url,
            "region": "77",
            "token": "c1d386c2416e54d5abd6cd5c01d26f59"
        }
        rs = request('POST', api, json=json)
        price = str(rs.json()['data']['price']).replace(',', '.')
        return price

    def price_utkonos(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        if soup.find('span', class_='product-sale-price title-l1 __accent ng-star-inserted'):
            price = soup.find('span', class_='product-sale-price title-l1 __accent ng-star-inserted').text
        else:
            price = soup.find('span', class_='product-sale-price title-l1 ng-star-inserted').text
        price = re.sub('[^0-9,]', '', price).replace(',', '.')
        return price

    def price_funduchok(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        if soup.find('input', class_='input input--radio'):
            price = soup.find('input', class_='input input--radio').get('data-price')
        else:
            price = soup.find('span', class_='product__card__options__action__value color--price-card').text
            price = re.sub('[^0-9,]', '', price).replace(',', '.')
        return price

    def price_vkusvill(self, url: str):
        rs = request(method='GET', url=url).text
        soup = BeautifulSoup(rs, "lxml")
        price = soup.find('span', class_='Price__value').text

        return price

    def compare(self, url, shop_name, product_id=None):
        methods = {
            'Фундучок': self.price_funduchok,
            'Экомаркет': self.price_ecomarket,
            'Утконос': self.price_utkonos,
            'Вкусвилл': self.price_vkusvill
        }
        if product_id:
            rf_price = self.price_rf(product_id)
            shop = methods[shop_name]
            shop_price = shop(url)
            different_price = Decimal(shop_price) - Decimal(rf_price)
            return {"different_price": different_price, "price": shop_price}
        else:
            shop = methods[shop_name]
            shop_price = shop(url)
            return {"price": shop_price}
