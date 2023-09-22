import requests
import os
import datetime as dt
import json
import time
from flight_data import FlightData

KIWI_APIKEY = os.environ["KIWI_APIKEY"]
SEARCH_HEADERS = {"apikey": KIWI_APIKEY}


class FlightSearch:
    """
    This class is responsible for talking to the Flight Search API.
    """

    def get_iata_code(self, city_name):
        search_url = "https://api.tequila.kiwi.com/locations/query"

        search_params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=search_url, headers=SEARCH_HEADERS, params=search_params)
        response.raise_for_status()
        response_json = response.json()
        self.city_iata_code = response_json["locations"][0]["code"]
        return self.city_iata_code

    def basic_flight_search(self, origin_city_code, destination_city_code, from_time, to_time, max_stopovers,
                            curr_time):
        search_url = "https://api.tequila.kiwi.com/v2/search"
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 7,
            "ret_from_diff_city": "false",
            "ret_to_diff_city": "false",
            "adults": 2,
            "children": 1,
            "selected_cabins": "M",
            "adult_hand_bag": "1,1",
            "child_hand_bag": 1,
            "only_working_days": "false",
            "only_weekends": "false",
            "one_for_city": 0,
            "one_per_date": 0,
            "max_stopovers": max_stopovers,
            "vehicle_type": "aircraft",
            "curr": "GBP",
            "locale": "en",
            "limit": 3,
        }

        response = requests.get(
            url=search_url,
            headers=SEARCH_HEADERS,
            params=params
        )

        time.sleep(5)

        try:
            data = response.json()["data"][0]
            # data = response.json()
        except IndexError:
            print(f"No flights with your parameters to {destination_city_code}")
            return None

        # Write json to file
        with open(f"search_results/{curr_time}-{destination_city_code}.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        # Use data with FlightData
        flight_data = FlightData(
            price=data["price"],
            origin_airport=data["flyFrom"],
            destination_city=data["cityTo"],
            destination_airport=data["route"][0]["flyTo"],

            out_date=data["route"][0]["local_departure"].split("T")[0],
            out_time=data["route"][0]["local_departure"].split("T")[1],
            out_airline=data["route"][0]["airline"],
            out_flight_no=data["route"][0]["flight_no"],

            return_date=data["route"][1]["local_departure"].split("T")[0],
            return_time=data["route"][1]["local_departure"].split("T")[1],
            return_airline=data["route"][1]["airline"],
            return_flight_no=data["route"][1]["flight_no"]

        )

        print(f"{flight_data.origin_airport} - {flight_data.destination_city}({flight_data.destination_airport})"
              f" -- £{flight_data.price}")
        return flight_data
