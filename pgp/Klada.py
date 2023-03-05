from collections import defaultdict

import pandas as pd

from pgp.BaseCalculator import BaseCalculator


class Klada(BaseCalculator):
    def __init__(self):
        super().__init__(self)
        self.points: dict = defaultdict(lambda: 0)

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
        ret.index += 1
        return ret[["Name", "Points", "Races"]]

    @staticmethod
    def _split_disks(result: pd.DataFrame):
        classified = lambda s: s.replace(':', '').replace('.', '').isnumeric()
        rest = result.loc[result["Time"].apply(classified)]
        disks = result.loc[~ result["Time"].apply(classified)]
        return disks, rest

    def _give_klada(self, row):
        registration = row["RegNo"]
        self.points[registration] += 1
