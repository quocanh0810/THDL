import scrapy
import requests
import json
import os

class PhongVuSpider(scrapy.Spider):
    name = "phongvu"
    api_url = 'https://discovery.tekoapis.com/api/v2/search-skus-v2'
    headers = {'Content-Type': 'application/json'}
    
    payload_template = {
        "terminalId": 4,
        "page": 1,
        "pageSize": 40,
        "slug": "/c/man-hinh-may-tinh",
        "filter": {},
        "returnFilterable": [],
        "sorting": {
            "sort": "SORT_BY_PUBLISH_AT",
            "order": "ORDER_BY_DESCENDING"
        }
    }

    def start_requests(self):
        page = 1
        while True:
            payload = self.payload_template.copy()
            payload["page"] = page
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self.log(f"HTTPError: {e.response.status_code} - {e.response.text}")
                break

            data = response.json()
            products = data.get('data', {}).get('products', [])
            if not products:
                self.log(f'No products found on page {page}')
                break

            for product in products:
                if 'canonical' in product:
                    product_url = f"https://phongvu.vn/{product['canonical']}"
                    yield scrapy.Request(url=product_url, callback=self.parse_product)
            
            page += 1

    def parse_product(self, response):
        url_path = response.url.split("/")[-1]
        folder_name = 'web/phongvu'
        filename = os.path.join(folder_name, f"{url_path}.html")
        
        os.makedirs(folder_name, exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {filename}')
