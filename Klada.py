from collections import defaultdict

import pandas as pd

from oris.util import generate_fields


class Klada:
    def __init__(self):
        self.names: dict = {}
        self.points: dict = defaultdict(lambda: 0)
        self.races: dict = defaultdict(lambda: 0)

    def calculate(self, results):
        for result in [r for r in results if len(r) >= 3]:

            self.add_race(result)

            disks, rest = self._split_disks(result)

            for _, row in disks.iterrows():
                self._give_klada(row)
            #TODO check times are sorted
            if len(rest) >= 3:
                self._give_klada(rest.iloc[-1])

        return self.format_output()

    def format_output(self):
        ret = pd.DataFrame.from_dict(self.races, "index", columns=["Races"])
        ret["Points"] = self.points
        ret["Points"].fillna(0, inplace=True)
        ret["Name"] = ret.index
        ret["Name"].replace(self.names, inplace=True)
        ret["Points"] = ret["Points"].astype(int)
        ret = ret.sort_values(["Points", "Races", "Name"], ascending=[True, False, True])
        ret.reset_index(inplace=True, drop=True)
        return ret[["Name", "Points", "Races"]]


    def _give_klada(self, row):
        registration = row["RegNo"]
        self.points[registration] += 1

    def _split_disks(self, result: pd.DataFrame):
        classified = lambda s: s.replace(':', '').replace('.','').isnumeric()
        rest = result.loc[result["Time"].apply(classified)]
        disks = result.loc[~ result["Time"].apply(classified)]
        return disks, rest

    def add_race(self, results):
        for _, row in results.iterrows():
            registration = row["RegNo"]
            self.races[registration] += 1
            if registration not in self.names:
                self.names[registration] = row["Name"]
