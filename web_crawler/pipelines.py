# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import re

import pymongo

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
            file_name: str = item["url"].split('/')[-1]
            file_name = file_name if file_name.endswith(".html") else file_name + ".html"
            with open(os.path.join(self.error_dir, web.value, file_name), 'w') as f:
                f.write(item["data"])

        spider.logger.info(f"Got monitor: {monitor}")
        return monitor

class PreprocessPipeline:
    def process_item(self, item: Monitor, spider):
        # Size
        size_search = re.findall('\d+\.\d*|\.?\d+', item.size)
        if size_search:
            item.size = float(size_search[0])
        
        # Resolution
        reso_search = re.findall('\d+[\*x]\d+', item.reso.replace(" ",""))
        if reso_search:
            item.reso = reso_search[0].replace("*", "x")

        # LCD type
        item.lcd_type = item.lcd_type.strip()

        # Frequency
        freq_search = re.findall('\d+', item.freq)
        if freq_search:
            item.freq = int(freq_search[0])

        # Response rate
        rsp_search = re.findall('\d+', item.rsp_rate)
        if rsp_search:
            item.rsp_rate = int((rsp_search[0]).replace(" ", ""))

        # Luminance
        lumi_search = re.findall('\d+', item.lumi)
        if lumi_search:
            item.lumi = int((lumi_search[0]).replace(" ", ""))

        # Constrast rate
        if item.constr_rate != "":
            item.constr_rate = item.constr_rate.split(":")[0].replace(",","").replace(".","").strip()+":1"

        # Port
        if item.port != "":
            item.port = item.port.replace(" ", "").split(",")

        # Price
        if item.price in ("0", ""):
            item.price = None
        else:
            item.price = int(item.price)

        # Brand
        item.brand = item.brand.upper()

        return item
class MongoPipeline:
    collection_name = "scrapy_items"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item: Monitor, spider):
        if not item.isEmpty():
            c = self.db[self.collection_name] 

            # Check duplication
            if c.count_documents({"url": item.url}) == 0:
                c.insert_one(item.asdict())

        return item