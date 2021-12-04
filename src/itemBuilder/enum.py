from django_enumfield import enum


class ItemType(enum.Enum):
    CANDLE = 0
    SCRUBBRUSH = 1
    INCENSE = 2
    AMULET = 3
    CENOTAPH = 4
    FECES = 5
    ARROW = 6
    JUNK = 7



class ItemAction(enum.Enum):
    USE = 0
    GIVE = 1
    PLACE = 2
    TAKE = 3

