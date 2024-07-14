import requests
import json
import os

url = 'https://api.cellphones.com.vn/v2/graphql/query'

headers = {
    'Content-Type': 'application/json',
}

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

num_pages = 13

folder_name = 'web/cellphones'
os.makedirs(folder_name, exist_ok=True)
filename = os.path.join(folder_name, 'products.json')

all_products = []

for page in range(1, num_pages + 1):
    payload = payload_template.copy()
    payload["query"] = payload["query"].replace("page: 1", f"page: {page}")
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        continue  

    data = response.json()
    
    products = data.get('data', {}).get('products', [])
    if products is not None:
        all_products.extend(products)
        print(f'Page {page} - {len(products)} products')
    else:
        print(f'Not found page {page}')

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)
