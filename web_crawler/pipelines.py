# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from .items import Website
from .stalkers import Monitor, process_hacom, process_phongvu, process_phucanh


class ParsePipeline:
    def process_item(self, item, spider):
        item["data"] = item["data"].replace("\n", "")
        return item

class ExtractPipeline:
    error_dir = "logs/extract_pipeline/error"

    def open_spider(self, spider):
        for w in Website:
            os.makedirs(os.path.join(self.error_dir, w.value), exist_ok=True)

    def process_item(self, item, spider):
        web = item["web"]
        data = item["data"]
        monitor = Monitor()

        try:
            if web == Website.hacom:
                monitor = process_hacom(data)
            elif web == Website.phongvu:
                monitor = process_phongvu(data)
            elif web == Website.phucanh:
                monitor = process_phucanh(data)
            else:
                spider.logger.error(f"Got weird website: {web}. Only support: {[e.value for e in Website]}")
        except Exception as e:
            spider.logger.error(f"Extracting pipeline error: {e}")
            file_name: str = data["url"].split('/')[-1]
            file_name = file_name + ".html" if file_name.endswith(".html") else file_name
            with open(os.path.join(self.error_dir, web.value, file_name), 'w') as f:
                f.write(item["data"])

        spider.logger.info(f"Got monitor: {monitor}")
        return monitor

class MongoPipeline:
    def process_item(self, item, spider):
        pass