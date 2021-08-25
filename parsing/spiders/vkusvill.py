import re
import unicodedata

from scrapy.spiders import SitemapSpider

from parsing.methods import telegram_info


class VkusvillSpider(SitemapSpider):
    name = "vkusvill"
    sitemap_urls = ['https://vkusvill.ru/upload/sitemap/msk/sitemap_goods.xml',]
    articles = []

    def parse(self, response, **kwargs):
        if response.xpath('//img[@class="lazyload"]/@title').get() is not None:
            name = response.xpath('//img[@class="lazyload"]/@title').get()
            image_url = response.xpath('//img[@class="lazyload"]/@data-src').get()
            price = response.xpath('//span[@class="Price__value"]/text()').get()
            ves_and_year = response.xpath('//li[@class="Product__listItem"]/text()').getall()
            try:
                ed_izm = response.xpath('//span[@class="Price__unit"]/text()').getall()[1]
                ves = re.sub("[^0-9]", "", ves_and_year[1])
                goden = ves_and_year[0]
            except IndexError:
                print('0 значение')
            category_list = response.xpath('//span[@class="Breadcrumbs__link"]/a/@title').getall()
            id = response.xpath('//div[@class="Product__col Product__col--content js-product-cart js-datalayer-detail'
                                ' js-datalayer-catalog-list-item"]/@data-xmlid').get()
            self.articles.append(id)
            yield {
                'name': name,
                'ed_izm': ed_izm.replace(' ', '').replace('/', '').replace('\xa0\xa0', ''),
                'price': unicodedata.normalize('NFKD', price).replace(' ', ''),
                'ves': ves,
                'image_url': image_url,
                'url': response.url,
                'category': category_list,
                'article': id
            }
        else:

            pass

    def close(self, reason):

        telegram_info(self.name)



