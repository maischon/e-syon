import datetime as dt
from enum import Enum
from itertools import groupby

import pandas as pd

from Klada import Klada
from Skalper import Skalper
from oris.Oris import Oris
from oris.util import generate_fields

@generate_fields
class Club:
    id: int
    registration: str

    @classmethod
    def create(cls, club: dict):
        return cls(club["ID"], club["Abbr"])

class Category(Enum):
    MEN = 1,
    WOMAN = 2

    @staticmethod
    def from_str(category: str):
        if "H" in category.upper() or "M" in category.upper():
            return Category.MEN
        if "D" in category.upper() or "W" in category.upper():
            return Category.WOMAN
        raise Exception("Unknown category: " + category)

def _get_club(club_name: str, oris: Oris) -> Club:
    clubs = oris.getCSOSClubList()
    if club_name.upper() in clubs:
        return Club.create(clubs[club_name.upper()])
    matching_clubs = [value["ID"] for short, value in clubs.items() if club_name.upper() in value['Name'].upper()]
    if len(matching_clubs) == 1:
        return Club.create(matching_clubs[1])
    raise Exception("No club found for: " + club_name)


class RocenkaImpl:
    def __init__(self, club_ame: str):
        self.oris = Oris()
        self.my_club: Club = _get_club(club_ame, self.oris)
        self.year_results = {}

    # def test(self):
    #
    #     print(self.oris.get_event_list(all=True,
    #                                       my_club=self.my_club.id,
    #                                       date_from=dt.date(2022, 1, 1),
    #                                       date_to=dt.date(2022, 12, 31)
    #                                       ))
    #
    #     results = self._obtain_results([5558])
    #     relevant_results = self._filter_club_and_categories(results)
    #
    #     final_results = self._split_by_category(relevant_results)
    #
    #     results = [self._create_table(result) for result in final_results]
    #     ret = Klada().calculate(self.filter(results, Category.MEN))
    #     print(ret)

    def _calculate_larva(self, year):
        results = self._get_year_results(year)
        return Klada().calculate(self.filter(results, Category.WOMAN))

    def _calculate_klada(self, year):
        results = self._get_year_results(year)
        return Klada().calculate(self.filter(results, Category.MEN))

    def _calculate_skalper(self, year):
        results = self._get_year_results(year)
        # TODO
        return Skalper().calculate(self.filter(results, Category.MEN))

    def _calculate_skalperka(self, year):
        results = self._get_year_results(year)
        # TODO
        return Skalper().calculate(self.filter(results, Category.WOMAN))

    def _get_year_results(self, year: int) -> list[pd.DataFrame]:
        """
        Obtains results for given club and given year.
        :param year: integer specifying year
        :return: list of all results with club competitors per race and per category
        """
        if year not in self.year_results:
            self.year_results[year] = self._obtain_year_results(year)
        return self.year_results[year]

    def _obtain_year_results(self, year: int) -> list[pd.DataFrame]:
        events = self.oris.get_event_list(all=True,
                                          my_club=self.my_club.id,
                                          date_from=dt.date(year, 1, 1),
                                          date_to=dt.date(year, 12, 31)
                                          )

        results = self._obtain_results([event["ID"] for _, event in events.items()])

        #TODO make it more functional
        relevant_results = self._filter_club_and_categories(results)

        final_results = self._split_by_category(relevant_results)

        return [self._create_table(result) for result in final_results]

    def _obtain_results(self, event_ids):
        for event_id in event_ids:
            yield self.oris.get_event_rank_results(event_id)

    def _filter_club_and_categories(self, results):
        for result in results:
            if len(result) == 0:
                continue
            # TODO here could be logic for separating categories
            filtered_result = [r for _, r in result.items() if "21" in r["ClassDesc"] and self.my_club.registration in r["RegNo"][:3]]
            if len(filtered_result) > 0:
                yield filtered_result

    @staticmethod
    def _split_by_category(relevant_results):
        for results in relevant_results:
            for _, ret in groupby(results, lambda result: result["ClassID"]):
                yield list(ret)

    @staticmethod
    def _create_table(result: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(result)


    def filter(self, results, category: Category):
        return [r for r in results if Category.from_str(r.iloc[0]["ClassDesc"]) == category]
