from api import Rocenka
from pgp.RocenkaImpl import Category

if __name__ == '__main__':
    # print(Oris().get_event_list())
    # print(Oris().getCSOSClubList())

    r = Rocenka("PGP")
    r.load(2022)
    # r.test()
    # print(r.calculate_skalper(2022))
    # print(r.calculate_larva(2022))
    print(r.calculate_obeslo(2022), Category.MEN)
    print(r.calculate_obeslo(2022), Category.WOMEN)
