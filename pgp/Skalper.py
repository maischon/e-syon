from collections import defaultdict
from itertools import product

import pandas as pd


class Skalper:

    def __init__(self):
        self.names: dict = {}
        self.defeated: dict = defaultdict(lambda: defaultdict(lambda: 0))

    def calculate(self, results):
        for result in results:

            #TODO check times are sorted

            self._register_defeats(result)

        return self._calculate_output()

    def _register_defeats(self, result):
        for index, row in result.iterrows():
            self._put_name(row)
            registration = row["RegNo"]
            for _, defeated in result.loc[index:]:
                self.defeated[registration][defeated["RegNo"]] += 1

    def _put_name(self, row):
        registration = row["RegNo"]
        if registration not in self.names:
            self.names[registration] = row["Name"]

    def _calculate_output(self):
        df = pd.DataFrame(columns=self.names, index=self.names)

        def result(first, second):
            if first == second:
                return ""
            return "{}:{}".format(
                self.defeated[first][second],
                self.defeated[second][first]
            )

        for i,j in product(range(len(df)), range(len(df))):
            df.iloc[i,j] = result(df.columns[i], df.index[j])

        # switch registration numbers to names
        df.columns = [self.names[c] for c in df.columns]
        df.index = [self.names[c] for c in df.index]

        # TODO sort by results
        return df
