import pandas as pd

from pgp.BaseCalculator import BaseCalculator


class Skalper(BaseCalculator):

    def calculate(self, results):
        for result in results:
            # TODO count only not disks? or finished?
            self.add_race(result)
        return self.format_output()

    def format_output(self):
        # TODO this code could be deduplicated as well
        ret = pd.DataFrame.from_dict(self.races, "index", columns=["Races"])
        ret["Name"] = ret.index
        ret["Name"].replace(self.names, inplace=True)
        ret = ret.sort_values(["Points", "Races", "Name"], ascending=[True, False, True])
        ret.reset_index(inplace=True, drop=True)
        return ret[["Name", "Races"]]
