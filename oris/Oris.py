
import requests
# import faster_than_requests as requests
import json
import datetime as dt
from util import generate_fields

@generate_fields
class Oris:
    is_verbose: Boolean = true
    # static variables:
    BASE_URL = r'https://oris.orientacnisporty.cz/API/?method=%s&format=%s'


    @staticmethod
    def _get(params: dict, format: str= 'json'):
        try:
            ret = requests.get(BASE_URL % (method, format), params=params)
            ret.raise_for_status()
            ret = ret.json()
            if ret['Status'] != 'OK':
                raise Exception(ret['Status'])
        except Exception as e:
            if is_verbose:
                print('Error: ' + str(e))
            return None
        return ret['Data']


    @staticmethod
    def _date2str(date: dt.datetime):
        if date is None:
            return ""
        return date.strftime('%Y-%m-%d')


    @staticmethod
    def _str2date(date: str):
        if date is None:
            return None
        return dt.datetime.strptime(date, '%Y-%m-%d')


    @staticmethod
    def _str2timedelta(str):
        try:
            s = str.split(':')
            if len(s) == 1:
                return dt.timedelta(seconds=int(s))
            if len(s) == 2:
                return dt.timedelta(minutes=int(s[0]),seconds=int(s[1]))
            if len(s) == 3:
                return dt.timedelta(hours=int(s[0]), minutes=int(s[1]),seconds=int(s[2]))
            raise Exception(str)
        except Exception as e:
            if VERBOSE:
                print(e)
        return dt.timedelta()

    @staticmethod
    def _str2time(str):
        try:
            # if str == '' or str == 'DISK':
            s = str.split(':')
            if len(s) == 1:
                return dt.time(second=int(s))
            if len(s) == 2:
                return dt.time(minute=int(s[0]), second=int(s[1]))
            if len(s) == 3:
                return dt.time(hour=int(s[0]), minute=int(s[1]), second=int(s[2]))
            raise Exception(str)
        except Exception as e:
            if is_verbose:
                print(e)
        return dt.time()


    @staticmethod
    def i_dont_know_what_that_is():
        for enum in ['region', 'discipline', 'sport', 'level', 'sourcetype']:
            e = Get('getList', {'list': enum})
            attribs = e.values().__iter__().__next__()
            for k in attribs:
                if 'Desc' in k:
                    name = k
                    break

            locals()[enum] = {value[name]: value['ID'] for _, value in e.items()}
