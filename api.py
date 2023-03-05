from pgp.RocenkaImpl import RocenkaImpl, Category
import datetime as dt


class Rocenka(RocenkaImpl):
    def __init__(self, club_name: str): super().__init__(club_name)

    def load(self, year: int = dt.datetime.now().year):
        return self._load(year)

    def calculate_obeslo(self, category: Category):
        """
        Calculates larva for given year.
        :return: Table containing larva
        """
        return self._calculate_obeslo(category)

    def calculate_klada(self, category: Category):
        """
        Calculates klada or larva for given year.
        """
        return self._calculate_klada(category)

    def calculate_skalper(self, category: Category):
        """
        Calculates skalper for given year and given category.
        """
        return self._calculate_skalper(category)