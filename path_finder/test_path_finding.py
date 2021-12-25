import sys
import os
from itertools import permutations
import pytest
from . import PathFinder


@pytest.fixture
def path_finder_obj():
    assert os.path.exists('../data/data.csv'), \
        "Path '../data/data.csv' does not exist!"
    return PathFinder('../data/data.csv', 'cp1251')


@pytest.fixture
def paths_map(path_finder_obj):
    return path_finder_obj.get_paths_map()


def test_paths_exist(path_finder_obj, paths_map):
    all_cities = set(path_finder_obj.df[path_finder_obj.origin_field]) \
                 | set(path_finder_obj.df[path_finder_obj.destination_field])
    for city_1, city_2 in permutations(all_cities, 2):
        path = path_finder_obj.find_path(city_1, city_2)
        computed_price = 0 if path.stages else sys.maxsize
        prev = city_1.lower()
        for cur_city in path.stages[1:]:
            computed_price += paths_map[prev][cur_city.lower()]
            prev = cur_city.lower()
        assert computed_price == path.price, \
            f"""Error while computing path from '{city_1}' to '{city_2}'! 
              Path: {path}, declared price: {path.price}, 
              in fact: {computed_price}"""


def test_comparison_with_straight_path(path_finder_obj, paths_map):
    for v, v_paths in paths_map.items():
        for neigh, direct_flight_price in v_paths.items():
            path = path_finder_obj.find_path(v, neigh)
            assert path.price <= direct_flight_price, \
                f""" Error while computing paths from '{v}' to '{neigh}'!
                  Straight flight price: {direct_flight_price}, 
                  minimal cost from algorithm: {path.price}"""
