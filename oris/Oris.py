import requests
# import faster_than_requests as requests
import json
import datetime as dt
from .util import generate_fields
from .constants import Sport, Region, Level


@generate_fields
class Oris:
    my_club: int = None
    is_verbose: bool = True
    # static variables:
    BASE_URL = r'https://oris.orientacnisporty.cz/API/?method=%s&format=%s'

    """
      - getEventList    - kalendář závodů
                        - nepovinné parametry:
                                  'all':      pokud je nastaveno all=1 pak zobrazí i ostatní závody
                                              mimo oficiální kalendář
                                  'name':     část názvu závodu
                                  'sport':    id sportu ... 1=OB, 2=LOB, 3=MTBO, 4=TRAIL
                                              (lze zadat více hodnot oddělených čárkou)
                                  'rg':       zkratka regionu např. HA, P, MSK, ...
                                  'level':    id úrovně (lze zadat více hodnot oddělených čárkou)
                                  'datefrom': datum od ve formátu RRRR-MM-DD
                                              (pokud není zadáno, pak se používá první den aktuálního roku)
                                  'dateto':   datum do ve formátu RRRR-MM-DD
                                              (pokud není zadáno, pak se používá poslední den aktuálního roku)
                                  'club':     id pořádajícího klubu
                                  'myClubId': id klubu pro zobrazení počtu přihlášek a výsledků
        příklad: https://oris.orientacnisporty.cz/API/?format=xml&method=getEventList
        lze použít i getEventListVersions se stejnými parametry (vrací pouze ID a verzi záznamu)

    """
    def get_event_list(self,
                       all: int = 0,
                       name: str = None,
                       sport: Sport = Sport.OB,
                       region: Region = Region.CR,
                       level: Level = None,
                       date_from: dt.date = None,
                       date_to: dt.date = None,
                       club: str = None,
                       my_club: int = None
                       ):
        return self._get(
            method="getEventList",
            params={
                'all': all,
                'name': name,
                'sport': None if sport is None else sport.value,
                'rg': None if region is None else region.value,
                'level': None if level is None else level.value,
                'datefrom': self._date2str(date_from),
                'dateto': self._date2str(date_to),
                'club': club,
                'myClubId': my_club,
            }
        )

    def _get(self, method: str, params: dict, format: str = 'json'):
        filtered_params = {k: v for k, v in params.items() if v is not None}
        try:
            request = self.BASE_URL % (method, format)
            if self.is_verbose:
                print("Requesting: " + str(request) + " with parameters "+ str(filtered_params))
            ret = requests.get(request, params=params)
            ret.raise_for_status()
            ret = ret.json()
            if ret["Status"] != "OK":
                raise Exception(ret['Status'])
        except Exception as e:
            if self.is_verbose:
                print('Error: ' + str(e))
                print("On request " + ret.request.url)
            return None
        return ret['Data']

    @staticmethod
    def _date2str(date: dt.date):
        if date is None:
            return None
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def _str2date(date: str) -> dt.date:
        if date is None:
            return None
        return dt.datetime.strptime(date, '%Y-%m-%d').date()

    @staticmethod
    def _str2timedelta(self, delta: str):
        try:
            s = delta.split(':')
            if len(s) == 1:
                return dt.timedelta(seconds=int(s))
            if len(s) == 2:
                return dt.timedelta(minutes=int(s[0]), seconds=int(s[1]))
            if len(s) == 3:
                return dt.timedelta(hours=int(s[0]), minutes=int(s[1]), seconds=int(s[2]))
            raise Exception(str)
        except Exception as e:
            if self.is_verbose:
                print(e)
        return dt.timedelta()

    @staticmethod
    def _str2time(self, time: str):
        try:
            # if str == '' or str == 'DISK':
            s = time.split(':')
            if len(s) == 1:
                return dt.time(second=int(s))
            if len(s) == 2:
                return dt.time(minute=int(s[0]), second=int(s[1]))
            if len(s) == 3:
                return dt.time(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
            raise Exception(str)
        except Exception as e:
            if self.is_verbose:
                print(e)
        return dt.time()

    @staticmethod
    def i_dont_know_what_that_is(self):
        #TODO probably check enums
        for enum in ['region', 'discipline', 'sport', 'level', 'sourcetype']:
            e = self._get('getList', {'list': enum})
            attribs = e.values().__iter__().__next__()
            for k in attribs:
                if 'Desc' in k:
                    name = k
                    break

            locals()[enum] = {value[name]: value['ID'] for _, value in e.items()}
