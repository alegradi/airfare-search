import requests
import os
import datetime as dt
import json

KIWI_APIKEY = os.environ["KIWI_APIKEY"]

departure_airport = "MAN"

date_time = dt.datetime.now()
date_time_now = date_time.strftime("%Y-%m-%d-%H-%M-%S")
today = dt.datetime.today()
today_plus_one = today + dt.timedelta(days=1)
tomorrow = today_plus_one.strftime("%d/%m/%Y")
today_plus_six_months = today + dt.timedelta(days=180)
six_months_later = today_plus_six_months.strftime("%d/%m/%Y")

# https://tequila.kiwi.com/portal/docs/tequila_api/search_api

search_url = "https://api.tequila.kiwi.com/v2/search"
search_headers = {
    "apikey": KIWI_APIKEY
}
search_params = {
    "vehicle_type": "aircraft",
    "curr": "GBP",
    "locale": "en",
    "fly_from": departure_airport,
    "fly_to": "FAO",
    "date_from": tomorrow,
    "date_to": six_months_later,
    "nights_in_dst_from": 5,
    "nights_in_dst_to": 7,
    "max_fly_duration": 14,
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
    "limit": 10
}

print(search_params)

response = requests.get(url=search_url, headers=search_headers, params=search_params)
response.raise_for_status()
data = response.json()

# write json to file
with open(f"search_results/{date_time_now}-{departure_airport}.json", "w") as data_file:
    json.dump(data, data_file, indent=4)

