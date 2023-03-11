from api import Rocenka
from pgp.RocenkaImpl import Category

if __name__ == '__main__':
    # print(Oris().get_event_list())
    # print(Oris().getCSOSClubList())

    r = Rocenka("PGP")
    r.load(2022)
    # r.test()
    print(r.calculate_skalper(year=2022, category=Category.MEN))
    # print(r.calculate_obeslo(year=2022, category=Category.WOMEN))
