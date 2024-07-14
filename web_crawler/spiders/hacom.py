import json
import os
import scrapy
import time

class HacomSpider(scrapy.Spider):
    name = "hacom"

    with open('web/hacom/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    start_urls = [f"https://hacom.vn{product['productUrl']}" for product in products if 'productUrl' in product]

    def parse(self, response):
        url_path = response.url.split("/")[-1]
        filename = f"web/hacom/{url_path}.html"
        
        os.makedirs('web/hacom', exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {filename}')
        time.sleep(2)
