from enum import Enum

REGION = {'CECHY': 'Č', 'CR': 'ČR', 'HANA': 'HA', 'VJC': 'JČ', 'JESTEDSKA': 'JE', 'JIHOMORAVSKA': 'JM',
          'MORAVA': 'M', 'MORAVSKOSLEZSKA': 'MSK', 'PRAZSKA': 'P', 'STREDOCESKA': 'StČ', 'VALASSKA': 'VA',
          'BEDOV': 'VČ', 'VYSOCINA': 'VY', 'ZAPADOCESKA': 'ZČ'}
DISCIPLINE = {'LONG': '1', 'MIDDLE': '2', 'SPRINT': '3', 'ULTRALONG': '4', 'RELAY': '5',
              'TEAMS': '6', 'SCORELAUF': '7', 'NOB': '9', 'RANKINGS': '10',
              'TEMPO': '11', 'SEMINARS': '12', 'STAGE_RACE': '13', 'MASS_START': '14'}
SPORT = {'OB': '1', 'LOB': '2', 'MTBO': '3', 'TRAIL': '4'}
LEVEL = {'MCR': '1', 'ZA': '2', 'ZB': '3', 'OZ': '4',
         'ETAP': '5', 'OTHER': '6', 'CPS': '7', 'CP': '8',
         'CLUBS': '9', 'SPRINT_CUP': '10', 'OZ_CHAMPS': '11', 'WRE': '12',
         'WINTER': '13', 'UNOFFICIAL': '14', 'SEMINARS': '15', 'STAGE_RACE': '16'}

# TODO rewrite to usable:
SOURCE_TYPE = {'Rozpis': '1', 'Pokyny': '2', 'Startovka': '3', 'Výsledky': '4', 'Plánek shromaždiště': '5',
               'Mezičasy': '6', 'Fotky': '7', 'Video': '8', 'Ukázky mapy': '9', 'Stará mapa': '10',
               'OB Postupy': '11', 'Startovka po klubech': '12', 'Web závodu': '13', 'Výsledky pro ranking': '14',
               'Výsledky pro žebříček': '15', 'Výsledky kategorie': '16', 'Výsledky pro žebříček A,B': '17',
               'Výsledky pro ranking veteránů': '18'}

# TODO rewrite to explicite enums:
Region = Enum("Region", REGION)
Discipline = Enum("Discipline", DISCIPLINE)
Sport = Enum("Sport", SPORT)
Level = Enum("Level", LEVEL)
SourceType = Enum("SourceType", SOURCE_TYPE)