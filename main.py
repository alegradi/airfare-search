from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from time_date import Time

# Constants
ORIGIN_CITY_CODE = "MAN"
AIRFARE_SUMMARY = ""

# Objects
data_manager = DataManager()
sheet_data = data_manager.get_sheet_data()
flightsearch = FlightSearch()
time = Time()

print(sheet_data)

# Verify if we have IATA code for the target destination in the spreadsheet
for item in sheet_data:
    # if len(item["iataCode"]) == 0:
    if item["iataCode"] == 0:
        print(f'{item["city"]} - no IATA Code')
        iata_code = flightsearch.get_iata_code(item["city"])
        # print(iata_code)  # Debug info

        item["iataCode"] = iata_code
        json_data = {"price": item}  # The sheet is 'prices' but Sheety expects singular 'price'
        # print(json_data)  # Debug info
        data_manager.update_sheet_data(json_data)

# Search for direct flights, no baggage specified
print(f"\nSearching for direct flights, no check-in luggage.")
AIRFARE_SUMMARY += f"Direct flights from: {ORIGIN_CITY_CODE}, 2 adults, 1 child, min 3 days, max 7 days, no luggage:"
for item in sheet_data:
    search_data = flightsearch.basic_flight_search(
        origin_city_code=ORIGIN_CITY_CODE,
        destination_city_code=item["iataCode"],
        from_time=time.tomorrow,
        to_time=time.date_six_months_from_now,
        max_stopovers=0,
        curr_time=time.date_time
    )

    if hasattr(search_data, "price"):
        matching_flight = (f"\n-----"
                           f"\n{search_data.origin_airport} -"
                           f" {search_data.destination_city}({search_data.destination_airport}) -"
                           f" £{search_data.price}"
                           f"\n{search_data.out_date} - {search_data.out_time} ->"
                           f" {search_data.out_airline}-{search_data.out_flight_no}"
                           f"\n{search_data.return_date} - {search_data.return_time} ->"
                           f" {search_data.return_airline}-{search_data.return_flight_no}")

        AIRFARE_SUMMARY += matching_flight

print(AIRFARE_SUMMARY)

