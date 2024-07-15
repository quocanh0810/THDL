import requests
import scrapy

from ..items import Website


class HacomSpider(scrapy.Spider):
    name = "hacom"
    api_url = 'https://hacom.vn/ajax/get_json.php'
    headers = {'Content-Type': 'application/json'}
    
    payload_template = {
        'action': 'product',
        'action_type': 'product-list',
        'category': '1589',
        'show': 40,
        'page': 1
    }

    def start_requests(self):
        page = 1
        while True:
            params = self.payload_template.copy()
            params['page'] = page
            response = requests.get(self.api_url, headers=self.headers, params=params)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                self.log(f"HTTPError: {e.response.status_code} - {e.response.text}")
                break

            data = response.json()
            products = data.get('list', [])
            if not products:
                self.log(f'No products found on page {page}')
                break

            for product in products:
                if 'productUrl' in product:
                    product_url = f"https://hacom.vn{product['productUrl']}"
                    yield scrapy.Request(url=product_url, callback=self.parse_product)
            
            page += 1

    def parse_product(self, response):
        yield {"web": Website.cellphones, "data": response.text}
        