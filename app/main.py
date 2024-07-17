from collections import defaultdict

import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def init_connection():
    return MongoClient("mongodb://mongo:password@localhost:27017/")


mongo = init_connection()
database = mongo["items"]
collection = database["scrapy_items"]  # Assuming collection name
search_fields = {
    "size": {"type": "int", "label": "Size (inch)"},  # Field information
    "price": {"type": "int", "label": "Price (VND)"},  # Price as integer
}

def search_monitors(filters):
  filter_dict = {}
  for field, field_info in filters.items():
    filter_dict[field] = {"$gte": field_info[0], "$lte": field_info[1]}

  return list(collection.find(filter_dict))

@st.cache_data(ttl=60)
def get_search_range():
    res = defaultdict(dict)
    for field in search_fields.keys():
        res[field]["min"] = (
            collection.find({}, {field: 1}).sort({field: 1}).limit(1).next()[field]
        )
        res[field]["max"] = (
            collection.find({}, {field: 1}).sort({field: -1}).limit(1).next()[field]
        )

    return res


# Initialize filter dictionary with empty values
filters = defaultdict(list)
search_range = get_search_range()
for field, field_info in search_fields.items():
    # Slider for numeric filters (price)
    filters[field] = st.sidebar.slider(
        f"{field_info['label']} Range",
        value=[
          search_range[field]["min"],
          search_range[field]["max"]
        ],
    )

st.title("Buy a Monitor!!!")

# Perform search if query is not empty
if st.button("Search"):
    results = search_monitors(filters)

    if results:
        st.subheader("Search Results:")
        for monitor in results:
            container = st.container(border=True)
            col = container.columns(2)
            
            col[0].write(f"**Size:** {monitor['size']} Inch")
            col[0].write(f"**Price:** {monitor['price']} VND")
            col[0].write(f"**Brand:** {monitor['brand']}")
            col[0].write(f"**Resolution:** {monitor['reso']}")
            col[0].write(f"**LCD:** {monitor['lcd_type']}")
            col[0].write(f"**Frequency:** {monitor['freq']} Hz")
            col[0].write(f"**Luminance:** {monitor['lumi']} nits")

            col[0].write(f"[Product Page]({monitor['url']})")  # Link to product page
            col[1].image(monitor['img'])
