# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from enum import Enum

import scrapy


class Website(Enum):
    phongvu = 1
    hacom = 2
    phucanh = 3

class WebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
