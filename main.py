from api import Rocenka
from pgp.RocenkaImpl import Category

if __name__ == '__main__':
    r = Rocenka("PGP")
    r.download()
    print(r.calculate_skalper(category=Category.MEN))
    print(r.calculate_skalper(category=Category.WOMEN))
    print(r.calculate_obeslo(category=Category.MEN))
    print(r.calculate_obeslo(category=Category.WOMEN))
    print(r.calculate_klada(category=Category.MEN))
    print(r.calculate_klada(category=Category.WOMEN))
    # r.export()
