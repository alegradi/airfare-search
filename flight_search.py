import requests
import os
import datetime as dt
import json
import time

KIWI_APIKEY = os.environ["KIWI_APIKEY"]


class FlightSearch:
    """
    This class is responsible for talking to the Flight Search API.
    """

    def __init__(self):
        self.departure_airport = "MAN"
        self.destination_airport = ""

        # Date and time
        self.date_time = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        date_tomorrow = dt.datetime.today() + dt.timedelta(days=1)
        self.tomorrow = date_tomorrow.strftime("%d/%m/%Y")
        date_six_months_from_now = dt.datetime.today() + dt.timedelta(days=180)
        self.date_six_months_from_now = date_six_months_from_now.strftime("%d/%m/%Y")

        # Search attributes
        self.search_headers = {
            "apikey": KIWI_APIKEY
        }
        self.search_params = ""

    def find_iata(self, city_name):
        search_url = "https://api.tequila.kiwi.com/locations/query"

        search_params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=search_url, headers=self.search_headers, params=search_params)
        response.raise_for_status()
        response_json = response.json()
        self.city_iata = response_json["locations"][0]["code"]
        return self.city_iata

    def basic_flight_search(self, destination_airport):
        search_url = "https://api.tequila.kiwi.com/v2/search"
        self.search_params = {
            "fly_from": self.departure_airport,
            "fly_to": destination_airport,
            "date_from": self.tomorrow,
            "date_to": self.date_six_months_from_now,
            "nights_in_dst_from": 5,
            "nights_in_dst_to": 7,
            "ret_from_diff_city": "false",
            "ret_to_diff_city": "false",
            "adults": 2,
            "children": 1,
            "selected_cabins": "M",
            "adult_hold_bag": "1,0",
            "adult_hand_bag": "1,1",
            "child_hold_bag": 1,
            "child_hand_bag": 1,
            "only_working_days": "false",
            "only_weekends": "false",
            "one_for_city": 0,
            "one_per_date": 0,
            "vehicle_type": "aircraft",
            "curr": "GBP",
            "locale": "en",
            "limit": 3
        }

        response = requests.get(url=search_url, headers=self.search_headers, params=self.search_params)
        response.raise_for_status()
        self.data = response.json()

        # write json to file
        with open(f"search_results/{self.date_time}-{destination_airport}.json", "w") as data_file:
            json.dump(self.data, data_file, indent=4)

        time.sleep(5)  # To not exceed our API request/min allowance
        return self.data
