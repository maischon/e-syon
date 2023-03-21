from collections import defaultdict

import pandas as pd

from pgp.util import check_results_are_sorted


class Skalper:

    def __init__(self):
        self.names: dict = {}
        self.defeated: dict = defaultdict(lambda: defaultdict(lambda: 0))

    def calculate(self, results):
        for result in results:
            check_results_are_sorted(result)

            self._register_defeats(result)

        return self._calculate_output()

    def _register_defeats(self, result):

        # TODO - check disks (they are not defeats)

        for index, row in result.iterrows():
            self._put_name(row)
            registration = row["RegNo"]
            for _, defeated in result.loc[index:, :].iterrows():
                self.defeated[registration][defeated["RegNo"]] += 1

    def _put_name(self, row):
        registration = row["RegNo"]
        if registration not in self.names:
            self.names[registration] = row["Name"]

    def _calculate_output(self):
        df = pd.DataFrame(columns=self.names, index=self.names)
        scores = pd.DataFrame(0, index=self.names, columns=["Points", "Wins", "Defeats"])

        def result(first, second):
            return self.defeated[first][second], self.defeated[second][first]

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                a, b = result(df.columns[i], df.index[j])
                df.iloc[i, j] = "{}:{}".format(a, b)
                df.iloc[j, i] = "{}:{}".format(b, a)
                if a > b:
                    scores.loc[df.columns[i], "Points"] += 1
                if b > a:
                    scores.loc[df.index[j], "Points"] += 1
                scores.loc[df.columns[i], "Wins"] += a
                scores.loc[df.columns[i], "Defeats"] += b
                scores.loc[df.index[j], "Wins"] += b
                scores.loc[df.index[j], "Defeats"] += a

        scores["diff"] = scores["Wins"] - scores["Defeats"]

        df = df.join(scores)

        df.sort_values(by=["Points", "diff"], inplace=True, ascending=[False, False])
        df = df[df.index.tolist() + ["Points", "diff", "Wins", "Defeats"]]

        df["Score"] = df["Wins"].astype(str) + ":" + df["Defeats"].astype(str)
        df.drop(["Wins", "Defeats", "diff"], axis=1, inplace=True)

        # switch registration numbers to names
        df.index = [self.names[c] for c in df.index]
        df.columns = df.index.tolist() + ["Points", "Score"]

        return df
