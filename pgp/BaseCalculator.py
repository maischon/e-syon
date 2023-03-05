from collections import defaultdict

import pandas as pd


class BaseCalculator:
    def __init__(self):
        self.names: dict = {}
        self.races: dict = defaultdict(lambda: 0)

    def add_race(self, results):
        for _, row in results.iterrows():
            registration = row["RegNo"]
            self.races[registration] += 1
            if registration not in self.names:
                self.names[registration] = row["Name"]
