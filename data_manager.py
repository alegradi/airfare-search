import requests
import os
from pprint import pprint

SHEETY_BEARER = os.environ["SHEETY_BEARER"]
SHEETY_URL = os.environ["SHEETY_URL"]

SHEETY_HEADERS = {"Authorization": f"Bearer {SHEETY_BEARER}"}


class DataManager:
    """
    This class is responsible for talking to the Google Sheet.
    """
    def __init__(self):
        self.sheet_data = ""
        self.get_sheet_data()

    def get_sheet_data(self):
        response = requests.get(url=SHEETY_URL, headers=SHEETY_HEADERS)
        response.raise_for_status()
        self.sheet_data = response.json()

    def update_sheet_data(self, json):
        update_url = f"{SHEETY_URL}/{json['price']['id']}"  # The sheet is 'prices' but Sheety expects singular 'price'
        response = requests.put(url=update_url, headers=SHEETY_HEADERS, json=json)
        response.raise_for_status()
        self.update_sheet_response = response.json()
        # print(self.update_sheet_response)  # Debug info
