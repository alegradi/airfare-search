from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from time_date import Time

# Constants
ORIGIN_CITY_CODE = "MAN"

# Objects
data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()
flightsearch = FlightSearch()
time = Time()

print(sheet_data)

# Verify if we have IATA code for the target destination in the spreadsheet
for item in sheet_data:
    if len(item["iataCode"]) == 0:
        print(f'{item["city"]} - no IATA Code')
        iata_code = flightsearch.get_iata_code(item["city"])
        # print(iata_code)  # Debug info

        item["iataCode"] = iata_code
        json_data = {"price": item}  # The sheet is 'prices' but Sheety expects singular 'price'
        # print(json_data)  # Debug info
        data_manager.update_sheet_data(json_data)

# Search for direct flights, no baggage specified
print(f"\nSearching for direct flights, no check-in luggage.")
for item in sheet_data:
    search_data = flightsearch.basic_flight_search(
        origin_city_code=ORIGIN_CITY_CODE,
        destination_city_code=item["iataCode"],
        from_time=time.tomorrow,
        to_time=time.date_six_months_from_now,
        max_stopovers=0,
        curr_time=time.date_time
    )
    