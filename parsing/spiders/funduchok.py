import re

from scrapy.spiders import SitemapSpider
from w3lib.html import remove_tags

from parsing.methods import telegram_info
from parsing.request import send_products


class FunduchokSpider(SitemapSpider):
    name = "funduchok"
    sitemap_urls = ['https://xn--d1amhfwcd2a.xn--p1ai/sitemap.xml',]
    articles = []
    products = []

    def parse(self, response, **kwargs):
        price_xpath_many = response.xpath('//input[@class="input input--radio"]/@data-price')
        price_xpath_sale = response.xpath('//span[@class="price__value"]/text()')

        prod_name = response.xpath('//h1[@class="h1 text-align-left"]/text()').get()
        if response.xpath('//a[@class="product__card__gallery__element__image-link"]/@src').get():
            image_url = 'https://xn--d1amhfwcd2a.xn--p1ai' + \
                        response.xpath('//a[@class="product__card__gallery__element__image-link"]/@src').get()
        else:
            image_url = 'Отсутвует'
        if price_xpath_many:
            price = price_xpath_many.get()
            string_value = remove_tags(response.xpath("//span[@class='color--weight']").get())
            ves = string_value.replace(' кг', '').replace('/ ', '')
            ed_izm = re.sub('[^A-Za-z]', '', string_value)
        elif price_xpath_sale:
            price = price_xpath_sale.get()
            ves = None
            ed_izm = 'шт'
        else:
            price = response.xpath('//span[@class="product__card__options__action__value color--price-card"]/text()').get()
            price = re.sub("[^0-9]", "", price)
            ves = None
            ed_izm = 'шт'
        product_id = response.xpath('//input[@type="hidden"]/@value').get()
        category_list = response.xpath('//ul[@class="breadcrumb__list"]/li/a/span/text()').getall()
        category = '|'.join(category_list)
        href = response.url
        self.articles.append(product_id)
        product = {
            'name': prod_name,
            'price': price,
            'weight': ves,
            'unit': ed_izm,
            'image_url': image_url,
            'category': category,
            'url': href,
            'article': product_id,
            'shop_id': 1
        }
        self.products.append(product)

        yield product

    def close(self, reason):
        send_products(self.products)
        telegram_info(self.name)













