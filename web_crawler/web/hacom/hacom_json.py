import requests
import json
import os
import time

url = 'https://hacom.vn/ajax/get_json.php'
params = {
    'action': 'product',
    'action_type': 'product-list',
    'category': '1589',
    'show': 40,
    'page': 1
}

headers = {
    'Content-Type': 'application/json',
}

num_pages = 20  # Số trang cần lấy, bạn có thể thay đổi tùy theo số lượng trang thực tế

folder_name = 'web/hacom'
os.makedirs(folder_name, exist_ok=True)
filename = os.path.join(folder_name, 'products.json')

all_products = []

for page in range(1, num_pages + 1):
    params['page'] = page
    response = requests.get(url, headers=headers, params=params)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e.response.status_code} - {e.response.text}")
        continue

    data = response.json()
    
    products = data.get('list', [])
    if products:
        all_products.extend(products)
        print(f'Page {page} - {len(products)} products')
    else:
        print(f'Not found page {page}.')
    
    time.sleep(2)  # Sleep for 2 seconds to avoid IP blocking

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(all_products, f, ensure_ascii=False, indent=4)
