class FlightData:

    def __init__(self, price, origin_airport, destination_city, destination_airport, out_date, out_time, out_airline,
                 out_flight_no, return_date, return_time, return_airline, return_flight_no):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport

        # Outbound leg
        self.out_date = out_date
        self.out_time = out_time
        self.out_airline = out_airline
        self.out_flight_no = out_flight_no

        # Return leg
        self.return_date = return_date
        self.return_time = return_time
        self.return_airline = return_airline
        self.return_flight_no = return_flight_no
