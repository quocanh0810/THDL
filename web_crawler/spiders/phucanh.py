from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Website


class PhucanhSpider(CrawlSpider):
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
        yield {"web": Website.phucanh, "data": response.text, "url": response.url}
