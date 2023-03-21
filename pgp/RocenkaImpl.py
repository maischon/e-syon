import datetime as dt
import pickle
from enum import Enum
from itertools import groupby

import pandas as pd

from oris.Oris import Oris
from pgp.Klada import Klada
from pgp.Obeslo import Obeslo
from pgp.Ranking import Ranking
from pgp.Skalper import Skalper
from utils.util import generate_fields


@generate_fields
class Club:
    id: int
    registration: str

    @classmethod
    def create(cls, club: dict):
        return cls(club["ID"], club["Abbr"])


class Category(Enum):
    MEN = 1,
    WOMEN = 2


def from_str(category: str):
    if "H" in category.upper() or "M" in category.upper():
        return Category.MEN
    if "D" in category.upper() or "W" in category.upper():
        return Category.WOMEN
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

    # TODO delete
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

    def _load(self, year: int):
        self.year_results[year] = self._obtain_year_results(year)

    def _save_loaded_data(self):
        with open('tmp.pickle', 'wb') as f:
            pickle.dump(self.year_results, f)

    def _calculate_klada(self, year: int, category: Category):
        results = self._get_year_results(year)
        return Klada().calculate(self.filter(results=results, category=category))

    def _calculate_skalper(self, year: int, category: Category):
        results = self._get_year_results(year)
        return Skalper().calculate(self.filter(results=results, category=category))

    def _calculate_obeslo(self, year: int, category: Category):
        results = self._get_year_results(year)
        return Obeslo().calculate(self.filter(results=results, category=category))

    def _calculate_ranking(self, year: int, category: Category):
        results = self._get_year_results(year)
        # TODO
        return Ranking().calculate(self.filter(results=results, category=category))

    def _get_year_results(self, year: int) -> list[pd.DataFrame]:
        """
        Obtains results for given club and given year.
        :param year: integer specifying year
        :return: list of all results with club competitors per race and per category
        """
        if year not in self.year_results:
            raise Exception("You must load this year " + str(year) + " beforehand.")
        return self.year_results[year]

    def _obtain_year_results(self, year: int) -> list[pd.DataFrame]:
        events = self.oris.get_event_list(all=True,
                                          my_club=self.my_club.id,
                                          date_from=dt.date(year, 1, 1),
                                          date_to=dt.date(year, 12, 31)
                                          )

        results = self._obtain_results([event["ID"] for _, event in events.items()])

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

            filtered_result = [r for _, r in result.items() if
                               "21" in r["ClassDesc"] and self.my_club.registration in r["RegNo"][:3]]
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

    @staticmethod
    def filter(results, category: Category):
        return [r for r in results if from_str(r.iloc[0]["ClassDesc"]) == category]
