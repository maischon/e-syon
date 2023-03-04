from RocenkaImpl import RocenkaImpl
from oris.Oris import Oris
import datetime as dt


class Rocenka(RocenkaImpl):
    def __init__(self, club_name: str): super().__init__(club_name)

    def calculate_larva(self, year: int = dt.datetime.now().year):
        """
        Calculates larva for given year.
        :return: Table containing larva
        """
        return self._calculate_larva(year)

    def calculate_klada(self, year: int = dt.datetime.now().year):
        """
        Calculates klada for given year.
        :return: Table containing larva
        """
        return self._calculate_klada(year)

    def calculate_skalper(self, year: int = dt.datetime.now().year):
        """
        Calculates skalper for given year.
        :return: Table containing skalper
        """
        return self._calculate_skalper(year)


if __name__ == '__main__':
    # print(Oris().get_event_list())
    # print(Oris().getCSOSClubList())

    r = Rocenka("PGP")
    # print(r.calculate_skalper(2022))
    print(r.calculate_larva(2022))
    print(r.calculate_klada(2022))
