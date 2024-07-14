import json
import os
import scrapy
import time

class CellphonesSpider(scrapy.Spider):
    name = "cellphones"

    with open('web/cellphones/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    start_urls = [f"https://cellphones.com.vn/{product['general']['url_path']}" for product in products if 'general' in product and 'url_path' in product['general']]

    def parse(self, response):
        
        url_path = response.url.split("/")[-1]
        filename = f"web/cellphones/{url_path}.html"
        
        os.makedirs('web/cellphones', exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {filename}')
        time.sleep(2)
