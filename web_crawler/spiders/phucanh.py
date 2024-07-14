import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

class ScreensSpider(CrawlSpider):
    name = 'phucanh'
    allowed_domains = ['phucanh.vn']
    start_urls = ['https://www.phucanh.vn/man-hinh-may-tinh.html']

    rules = (
        # Rule link các sản phẩm
        Rule(LinkExtractor(restrict_xpaths='//li[@class="p-item-group "]//a[@class="p-img"]'), callback='parse_product', follow=True),
        # Rule link phân trang
        Rule(LinkExtractor(restrict_xpaths='//div[@class="paging"]//a'), follow=True),
    )

    def parse_product(self, response):
        domain = response.url.split("/")[2]
        folder_name = 'web/phucanh'

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        product_id = response.url.split("/")[-1].replace('.html', '')
        filename = os.path.join(folder_name, f'full_html_{product_id}.html')

        self.log(f'Saved file: {filename}')
        with open(filename, 'wb') as f:
            f.write(response.body)
