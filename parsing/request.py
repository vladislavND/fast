from requests import request


def send_products(products):
    rq = request(method='POST', url='http://127.0.0.1:8000/api/products', json=products)
    return rq.json()