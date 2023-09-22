import datetime as dt

class Time:
    """
    For all of our time needs.
    """
    def __init__(self):

        self.date_time = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        date_tomorrow = dt.datetime.today() + dt.timedelta(days=1)
        self.tomorrow = date_tomorrow.strftime("%d/%m/%Y")
        date_six_months_from_now = dt.datetime.today() + dt.timedelta(days=180)
        self.date_six_months_from_now = date_six_months_from_now.strftime("%d/%m/%Y")
