import argparse
import json
import os
import requests

from copy import copy
from itertools import combinations
from tqdm import tqdm

from constants import headers, default_params, uri, popular_directions


def get_tickets(month: str, year: str, output_fp: str):
    dir_pairs = combinations(popular_directions, 2)
    for pair in tqdm(list(dir_pairs)):
        custom_params = copy(default_params)
        custom_params.update(
            {"depart_date": f"{year}-{month}",
             "origin": pair[0],
             "destination": pair[1]}
        )
        response = requests.get(
            uri,
            params=custom_params,
            headers=headers
        )
        with open(os.path.join(output_fp, f"{year}-{month}-{pair[0]}-{pair[1]}.json"),
                  "w") as fd:
            json.dump(response.json(), fd, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--year',
        '-y',
        type=str,
        required=True,
        help=r'Departure year',
    )
    parser.add_argument(
        '--month',
        '-m',
        type=str,
        required=True,
        help='Departure month',
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        required=True,
        help='Output dir',
    )
    args = parser.parse_args()
    get_tickets(args.year, args.month, args.output)
    return 1


if __name__ == '__main__':
    main()
