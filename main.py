from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from web_crawler.spiders import HacomSpider, PhongVuSpider, PhucanhSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
# process.crawl(HacomSpider)
process.crawl(PhongVuSpider)
# process.crawl(PhucanhSpider)
process.start()