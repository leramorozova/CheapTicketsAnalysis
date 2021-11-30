import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from typing import List

from constants import AirportData


def parse_airports(amount_of_airports: int, sizes: List[str], verbose: bool) -> List[AirportData]:
    data = []

    iter_ = range(101) if verbose is False else tqdm(range(101))
    for i in iter_:
        response = requests.get("https://www.unipage.net/ru/airports",
                                params={
                                    "country_id[0]": 182,
                                    "page": i,
                                    "per-page": 10
                                    }
                                )

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            airport_data = AirportData(*cols, country="Russia")
            if airport_data.IATA and airport_data.size in sizes:
                data.append(airport_data)

            if len(data) > amount_of_airports:
                return data
    return data
