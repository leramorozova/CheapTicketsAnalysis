import os
import sys
import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, AnyStr, Tuple
import pandas as pd


@dataclass
class Path:
    price: int
    stages: Tuple[AnyStr]

    def __bool__(self):
        return bool(self.stages)

    def __str__(self):
        if not self:
            return "Path does not exists"
        return f"Price: {self.price}, route: " \
               f"{'->'.join(map(lambda s: s.capitalize(), self.stages))}"


class PathFinder:

    def __init__(self, df_path: str, encoding: str,
                 origin_field_name='origin_city',
                 destination_field_name='destination_city',
                 price_field_name='price'):

        assert os.path.exists(df_path), f"Path '{df_path}' does not exist!"
        assert encoding, f"Encoding should be set!"

        self.df = pd.read_csv(df_path, encoding=encoding)
        self.origin_field = origin_field_name
        self.destination_field = destination_field_name
        self.price_field = price_field_name

    def get_paths_map(self) -> DefaultDict[AnyStr, DefaultDict[AnyStr, int]]:
        min_price_df = self.df[
            [self.origin_field, self.destination_field, self.price_field]]\
            .groupby([self.origin_field, self.destination_field],
                     as_index=False).min()
        paths_map = defaultdict(lambda: defaultdict(lambda: sys.maxsize))
        for row in min_price_df.itertuples():
            paths_map[row[1].lower()][row[2].lower()] = row[3]
        return paths_map

    def find_path(self, v_from: AnyStr, v_to: AnyStr) -> Path:
        v_from = v_from.lower()
        v_to = v_to.lower()

        paths_map = self.get_paths_map()
        visited = set()
        dists = defaultdict(lambda: sys.maxsize)
        routes = defaultdict(tuple)

        queue = [(0, v_from)]
        dists[v_from] = 0
        routes[v_from] = (v_from,)

        while queue and v_to not in visited:
            cur_w, cur_v = heapq.heappop(queue)
            for v, w in paths_map[cur_v].items():
                if v not in visited and dists[v] > cur_w + w:
                    heapq.heappush(queue, (cur_w + w, v))
                    dists[v] = cur_w + w
                    routes[v] = routes[cur_v] + (v,)

            visited.add(cur_v)

        return Path(dists[v_to], routes[v_to])


