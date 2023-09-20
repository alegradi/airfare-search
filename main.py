from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch


# Init DataManager data
data_manager = DataManager()
sheet_data = data_manager.sheet_data["prices"]

pprint(sheet_data)

# Init FlightSearch
flightsearch = FlightSearch()

for item in sheet_data:
    if len(item["iataCode"]) == 0:
        print(f'{item["city"]} - no IATA Code')
        iata_code = flightsearch.find_iata(item["city"])
        # print(iata_code)  # Debug info

        item["iataCode"] = iata_code
        json_data = {"price": item}  # The sheet is 'prices' but Sheety expects singular 'price'
        print(json_data)  # Debug info
        data_manager.update_sheet_data(json_data)

    else:
        search_data = flightsearch.basic_flight_search(item["iataCode"])
        if search_data["_results"] == 0:
            print(f"No Luck with {item['iataCode']}")
        else:
            print(f"{item['city']} - {search_data['data'][0]['price']}")

# pprint(sheet_data)  # Debug info
