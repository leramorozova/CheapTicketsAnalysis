from credentials import TOKEN

popular_directions = [
    "BJS",  # Beijing
    "BUH",  # Bucharest
    "BUE",  # Buenos Aires
    "CHI",  # Chicago
    "JKT",  # Jakarta
    "LON",  # London
    "MIL",  # Milan
    "YMQ",  # Montreal
    "MOW",  # Moscow
    "NYC",  # New York City
    "OSA",  # Osaka
    "PAR",  # Paris
    "RIO",  # Rio de Janeiro
    "ROM",  # Rome
    "SAO",  # São Paulo
    "SPK",  # Sapporo
    "SEL",  # Seoul
    "STO",  # Stockholm
    "TCI",  # Tenerife
    "TYO",  # Tokyo
    "YTO",  # Toronto
    "WAS"  # Washington
]

date = "2019-11"
uri = 'https://api.travelpayouts.com/v1/prices/calendar'
default_params = {
    "depart_date": "2019-11",
    "origin": "MOW",
    "destination": "BCN",
    "calendar_type": "departure_date",
    "currency": "USD"
}

headers = {
  'X-Access-Token': TOKEN
}
