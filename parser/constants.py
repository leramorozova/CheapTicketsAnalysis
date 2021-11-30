import os
from collections import namedtuple


uri = 'https://api.travelpayouts.com/v1/prices/calendar'
default_params = {
    "depart_date": "2019-11",
    "origin": "MOW",
    "destination": "BCN",
    "calendar_type": "departure_date",
    "currency": "USD"
}

TOKEN = os.environ.get("AVIASALES_TOKEN")
if not TOKEN:
    raise KeyError("Not Authenticated: AVIASALES_TOKEN is not provided in env.")

headers = {
  'X-Access-Token': TOKEN
}

AirportData = namedtuple("AirportData", ["IATA", "ICAO", "name", "city", "flag", "size", "passengers", "country"])
