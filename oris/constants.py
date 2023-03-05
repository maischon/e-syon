from enum import Enum


class SourceType(Enum):
    BULLETIN1 = 1
    BULLETIN2 = 2
    START_LIST = 3
    RESULTS = 4
    CENTER_MAP = 5
    SPLITS = 6
    PHOTO = 7
    VIDEO = 8
    MAP_SAMPLES = 9
    OLD_MAP = 10
    OB_POSTUPY = 11
    STARTLIST_BY_CLUB = 12
    WEB = 13
    RANKING_RESULTS = 14
    RESULTS_FOR_ZEBRICEK = 15
    CATEGORY_RESULTS = 16
    RESULTS_FOR_ZEBRICEK_AB = 17
    RESULTS_VETERANKING = 18


class Level(Enum):
    MCR = 1
    ZA = 2
    ZB = 3
    OZ = 4
    ETAP = 5
    OTHER = 6
    CPS = 7
    CP = 8
    CLUBS = 9
    SPRINT_CUP = 10
    OZ_CHAMPS = 11
    WRE = 12
    WINTER = 13
    UNOFFICIAL = 14
    SEMINARS = 15
    STAGE_RACE = 16


class Sport(Enum):
    OB = 1
    LOB = 2
    MTBO = 3
    TRAIL = 4


class Discipline(Enum):
    LONG = 1
    MIDDLE = 2
    SPRINT = 3
    ULTRALONG = 4
    RELAY = 5
    TEAMS = 6
    SCORELAUF = 7
    NOB = 9
    RANKINGS = 10
    TEMPO = 11
    SEMINARS = 12
    STAGE_RACE = 13
    MASS_START = 14


class Region(Enum):
    CECHY = "Č"
    CR = "ČR"
    HANA = "HA"
    VJC = "JČ"
    JESTEDSKA = "JE"
    JIHOMORAVSKA = "JM"
    MORAVA = "M"
    MORAVSKOSLEZSKA = "MSK"
    PRAZSKA = "P"
    STREDOCESKA = "StČ"
    VALASSKA = "VA"
    BEDOV = "VČ"
    VYSOCINA = "VY"
    ZAPADOCESKA = "ZČ"
