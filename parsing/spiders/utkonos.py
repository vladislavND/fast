import scrapy
import requests

from parsing.methods import telegram_info


class UtkonosSpider(scrapy.Spider):
    name = 'utkonos'
    allowed_domains = ['www.utkonos.ru',]
    HEADERS = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryvOKTepCjBBVARAbu'}
    category = []
    articles = []

    def start_requests(self):
        url = 'https://www.utkonos.ru/api/v1/goodsCategoriesTreeByChildGet'
        data = '------WebKitFormBoundaryvOKTepCjBBVARAbu\r\nContent-Disposition: form-data; name="request"\r\n\r\n{"Head":{"DeviceId":"6D5103F931F6BF66890F21E966BC436B","Domain":"www.utkonos.ru","RequestId":"fd947996c73548e3f5fe1cb65ec88da8","MarketingPartnerKey":"mp-cc3c743ffd17487a9021d11129548218","Version":"angular_web_0.0.0","Client":"angular_web_0.0.0","Method":"goodsCategoriesTreeByChildGet","Store":"utk"},"Body":{"CatalogueId":"40"}}\r\n------WebKitFormBoundaryvOKTepCjBBVARAbu--\r\n'
        data_byte = data.encode()
        response = requests.post(url=url, data=data_byte, headers=self.HEADERS)
        response_data = response.json().get('Body').get('GoodsCategoryList')
        for data_response in response_data:
            self.category.append({data_response['Id']: data_response['Name']})
        yield scrapy.FormRequest(url='http://wikipedia.org', method='GET', callback=self.main)

    def main(self, *args):
        offset = 0
        for categories in self.category:
            for key, value in categories.items():
                while True:
                    count = 40
                    url = 'https://www.utkonos.ru/api/v1/goodsItemSearch'
                    data_string = '------WebKitFormBoundaryvOKTepCjBBVARAbu\r\nContent-Disposition: form-data; name="request"\r\n\r\n{"Head":{"DeviceId":"6D5103F931F6BF66890F21E966BC436B","Domain":"www.utkonos.ru","RequestId":"fd947996c73548e3f5fe1cb65ec88da8","MarketingPartnerKey":"mp-cc3c743ffd17487a9021d11129548218","Version":"angular_web_0.0.0","Client":"angular_web_0.0.0","Method":"goodsItemSearch","Store":"utk"},"Body":{"Return":{"LandingData":1,"Properties":1,"AllProperties":1,"GoodsCategoryTree":1,"GoodsCategoryList":0,"CatalogueFilters":1,"Banners":1},"Offset":'+ str(offset) +',"Filters":[],"OrderPreset":"category-popular","Count":'+ str(count) +',"addictive":false,"IncludePreorder":1,"CatalogueFilters":[],"ModelGrouping":0,"ModelGroupingInside":1,"GoodsCategoryId":'+ key +'}}\r\n------WebKitFormBoundaryvOKTepCjBBVARAbu--\r\n'
                    data = data_string.encode()
                    response = requests.post(url=url, headers=self.HEADERS, data=data)
                    offset += 40
                    if response.json().get('Body').get('GoodsItemList'):
                        response_data = response.json().get('Body').get('GoodsItemList')
                        for data_products in response_data:
                            self.articles.append(data_products['Id'])
                            yield {
                                'name': data_products['Name'],
                                'ed_izm': data_products['GoodsUnitList'][0]['UnitName'],
                                'ves': data_products['BruttoWeight'],
                                'category': value + ' | ' + data_products['DefaultCategoryName'],
                                'article': data_products['Id'],
                                'image_url': data_products['ImageBigUrl'],
                                'price': data_products['Price'],
                                'url': f'https://www.utkonos.ru/item/{data_products["OriginalId"]}/{data_products["Slug"]}'
                            }
                    else:
                        offset = 0
                        break

    def close(self, reason):
        telegram_info(self.name)










