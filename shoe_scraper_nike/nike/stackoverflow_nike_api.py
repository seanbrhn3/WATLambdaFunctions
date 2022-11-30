"""
Stole this from a stack overflow answer

https://stackoverflow.com/questions/62999427/how-to-webscrape-all-shoes-on-nike-page-using-python
"""

import requests
import json
import re

# your product page
uri = 'https://www.nike.com/w/shoes-y7ok'

base_url = 'https://api.nike.com'
session = requests.Session()

def get_lazy_products(stub, products):
#Get the lazily loaded products.
    response = session.get(base_url + stub).json()
    next_products = response['pages']['next']
    products += response['objects']
    if next_products:
        get_lazy_products(next_products, products)
    return products

# find INITIAL_REDUX_STATE
html_data = session.get(uri).text
print(re.search(r'window.INITIAL_REDUX_STATE=(\{.*?\});', html_data))
redux = json.loads(re.search(r'window.INITIAL_REDUX_STATE=(\{.*?\});', html_data).group(1))

# find the initial products and the api entry point for the recursive loading of additional products
wall = redux['Wall']
initial_products = re.sub('anchor=[0-9]+', 'anchor=0', wall['pageData']['next'])

# find all the products
products = get_lazy_products(initial_products, [])

# Optional: filter by id to get a list with unique products
cloudProductIds = set()
unique_products = []
for product in products:
    try:
        if not product['id'] in cloudProductIds:
            cloudProductIds.add(product['id'])
            unique_products.append(product)
    except KeyError:
        print(product)