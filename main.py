from api import Rocenka
from pgp.RocenkaImpl import Category

if __name__ == '__main__':
    r = Rocenka("PGP")
    r.download(2022)
    print(r.calculate_skalper(year=2022, category=Category.MEN))
    print(r.calculate_skalper(year=2022, category=Category.WOMEN))
    print(r.calculate_obeslo(year=2022, category=Category.MEN))
    print(r.calculate_obeslo(year=2022, category=Category.WOMEN))
    print(r.calculate_klada(year=2022, category=Category.MEN))
    print(r.calculate_klada(year=2022, category=Category.WOMEN))
