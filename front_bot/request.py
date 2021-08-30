from requests import request


class Request:

    def get_price(self, url) -> str:
        rs = request(url='http://localhost:8000/api/price', method='POST', json={'url': url})
        text = self.format_dict_to_string(rs.json())
        return text

    def get_all_price(self, article: str) -> str:
        rs = request(url=f'http://localhost:8000/api/price/{article}', method='GET')
        text = self.format_dict_to_string(rs.json())
        return text

    def format_dict_to_string(self, data: dict) -> str:
        msg = f"Наименование: {data.get('name')}\nЦена: {data.get('price')}\nМагазин: {data.get('shop')}\n" \
              f"Артикул: {data.get('article')}\nUrl: {data.get('url')}\nЦена со скидкой: {data.get('sale_price')}\n" \
              f"Разница в цене: {data.get('different_price')}"
        return msg

    def get_spiders(self) -> list:
        data = request(method='GET', url='http://localhost:8000/api/scrapyd/parsing')
        return data.json()

    def start_spider(self, spider: str):
        data = {'spider': spider}
        request(method='POST', url='http://localhost:8000/api/scrapyd/run', json=data)




