import os

import requests
from requests.models import Response


class BotRequest:
    def __init__(self):
        self.url = os.getenv('BASE_URL')

    def post(self, endpoint: str, data: dict = None) -> Response:
        response = requests.post(
            url=self.url + endpoint,
            json=data
        )
        return response

    def get(self, endpoint: str) -> Response:
        response = requests.get(
            url=self.url + endpoint
        )
        return response

    def send_processing_product(self, shop_id, file):
        file = requests.post(
            url=self.url + f'/api/processed_product_xlsx/{shop_id}',
            files={'file': ('report.xls', file, 'application/vnd.ms-excel',)}
        )
        return file.content


