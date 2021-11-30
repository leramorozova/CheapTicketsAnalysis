import os
import requests

import pandas as pd

from copy import copy
from itertools import combinations
from tqdm import tqdm
from typing import Dict, Tuple

from constants import headers, default_params, uri, AirportData
from parse_airports import parse_airports


def process_row(date: str, json_data: Dict[str, str],
                pair: Tuple[Tuple[AirportData]]):
    row = copy(json_data)
    row.update({
        "datetime": date,
        "origin_city": pair[0].city,
        "origin_country": pair[0].country,
        "destination_city": pair[1].city,
        "destination_country": pair[1].country
    })
    return row


def get_tickets(num_airports: int, airport_size,
                year_from: int = None, year_to: int = None, output_fp: str = ".",
                verbose: bool = True):
    result = []

    airports = parse_airports(num_airports, airport_size, verbose)
    for year in range(year_from, year_to):
        for month in range(1, 12):
            if verbose:
                print(f"Processing {year}-{month}...")

            dir_pairs = combinations(airports, 2)
            target_pairs = tqdm(list(dir_pairs)) if verbose else list(dir_pairs)

            for pair in target_pairs:
                custom_params = copy(default_params)
                custom_params.update(
                    {"depart_date": f"{year}-{month}",
                     "origin": pair[0].IATA,
                     "destination": pair[1].IATA}
                )
                response = requests.get(
                    uri,
                    params=custom_params,
                    headers=headers
                )
                if not response.ok:
                    if verbose:
                        print(f"Request failed: {response.content}")
                    continue

                data = response.json()
                if data["success"] is not True:
                    continue
                else:
                    data = data["data"]

                for key in data:
                    row = process_row(key, data[key], pair)
                    result.append(row)

            if verbose:
                print(f"Total count for {year}: {len(result)}")
                df = pd.DataFrame(result)
                df.to_csv(os.path.join(output_fp, "data.csv"))

    df = pd.DataFrame(result)
    return df.to_csv(os.path.join(output_fp, "data.csv"))
