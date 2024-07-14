import scrapy
import requests
import os

class CellphonesSpider(scrapy.Spider):
    name = "cellphones"
    api_url = 'https://api.cellphones.com.vn/v2/graphql/query'
    headers = {'Content-Type': 'application/json'}
    
    payload_template = {
        "query": """
            query {
                products(
                    filter: {
                        static: {
                            categories: ["784"],
                            province_id: 30,
                            stock: {
                                from: 0
                            },
                            stock_available_id: [46, 56, 152, 4164],
                            filter_price: {from: 0, to: 79990000}
                        },
                        dynamic: {
                        }
                    },
                    page: 1,
                    size: 20,
                    sort: [{view: desc}]
                ) {
                    general {
                        product_id
                        name
                        attributes
                        attributes
                        sku
                        doc_quyen
                        manufacturer
                        url_key
                        url_path
                        categories {
                            categoryId
                        }
                        review {
                            total_count
                            average_rating
                        }
                    },
                    filterable {
                        is_installment
                        stock_available_id
                        company_stock_id
                        filter {
                            id
                            Label
                        }
                        is_parent
                        exclusive_prices
                        price
                        prices
                        special_price
                        promotion_information
                        thumbnail
                        promotion_pack
                        sticker
                        flash_sale {
                            id
                            is_valid
                            shown_at
                        }
                    }
                }
            }
        """,
        "variables": {}
    }

    def start_requests(self):
        page = 1
        while(True):
            payload = self.payload_template.copy()
            payload["query"] = payload["query"].replace("page: 1", f"page: {page}")
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
                if 'general' in product and 'url_path' in product['general']:
                    product_url = f"https://cellphones.com.vn/{product['general']['url_path']}"
                    yield scrapy.Request(url=product_url, callback=self.parse_product)
            
            page += 1

    def parse_product(self, response):
        url_path = response.url.split("/")[-1]
        filename = f"web/cellphones/{url_path}.html"
        
        os.makedirs('web/cellphones', exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {filename}')
