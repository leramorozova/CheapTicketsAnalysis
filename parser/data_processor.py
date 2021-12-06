import os
import pandas
import requests

import numpy as np
import pandas as pd

from copy import copy
from itertools import combinations
from geopy.geocoders import Nominatim
from geopy import Point, distance
from tqdm import tqdm
from typing import Dict, Tuple

from parser.constants import headers, default_params, uri, AirportData
from parser.parse_airports import parse_airports


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


def get_tickets(num_airports: int, airport_size, output_fp: str = ".",
                verbose: bool = True):
    result = []

    print("Parsing available airports...")
    airports = parse_airports(num_airports, airport_size, verbose)
    dir_pairs = combinations(airports, 2)
    target_pairs = tqdm(list(dir_pairs)) if verbose else list(dir_pairs)

    print("Parsing tickets...")
    for pair in target_pairs:
        custom_params = copy(default_params)
        custom_params.update(
            {"origin": pair[0].IATA,
             "destination": pair[1].IATA}
        )
        response = requests.get(
            uri,
            params=custom_params,
            headers=headers
        )
        if not response.ok:
            if verbose:
                pass
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
        print(f"Total count for: {len(result)}")
        df = pd.DataFrame(result)
        df.to_csv(os.path.join(output_fp, "data.csv"))
        return df


def create_point(row, key):
    if str(row[f'{key}_city_lat']) != 'nan':
        return Point(str(row[f'{key}_city_lat']) + ' ' + str(row[f'{key}_city_lon']))
    else:
        return row


def find_distance(x):
    try:
        return distance.distance(x['destination_point'], x['origin_point']).km
    except Exception:
        return np.nan


def add_location_metadata(df: pandas.DataFrame):
    """
    Function extracts additional data on cities location and distance to dataframe.
    """
    geolocator = Nominatim(user_agent='andrew_v')

    all_cities = list(set(df['origin_city'].unique()) | set(df['destination_city'].unique()))
    cities_lat_dict = {}
    cities_lon_dict = {}
    cities_type_dict = {}
    cities_country_dict = {}
    not_found = []
    for city in all_cities:
        location = geolocator.geocode(city)
        if location:
            location_dict = location.raw
            cities_lat_dict[city] = location_dict['lat']

            if city != 'Mineralnyye Vody':
                cities_lon_dict[city] = location_dict['lon']
            else:
                cities_lon_dict[city] = '43.0909294469511'

            cities_type_dict[city] = location_dict['type']
            cities_country_dict[city] = location_dict['display_name'].split(',')[-1]

        else:
            if city == 'Mys Kamennyi':
                cities_lat_dict[city] = '68.46629314772403'
                cities_lon_dict[city] = '73.59525608730465'
                cities_type_dict[city] = '?'
                cities_country_dict[city] = 'Россия'
            else:
                not_found.append(city)
                print(f"Not found city: {city}")

    df['origin_city_lat'] = df['origin_city'].map(cities_lat_dict)
    df['origin_city_lon'] = df['origin_city'].map(cities_lon_dict)
    df['origin_city_type'] = df['origin_city'].map(cities_type_dict)
    df['origin_city_country'] = df['origin_city'].map(cities_country_dict)
    df['destination_city_lat'] = df['destination_city'].map(cities_lat_dict)
    df['destination_city_lon'] = df['destination_city'].map(cities_lon_dict)
    df['destination_city_type'] = df['destination_city'].map(cities_type_dict)
    df['destination_city_country'] = df['destination_city'].map(cities_country_dict)
    df['destination_point'] = df.apply(lambda x: create_point(x, 'destination'),
                                       axis=1)
    df['origin_point'] = df.apply(lambda x: create_point(x, 'origin'),
                                  axis=1)
    df['distance_origin_destination_km'] = df.apply(lambda x: find_distance(x), axis=1)
    return df
