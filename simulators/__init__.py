from enum import Enum, auto, IntEnum


class RollResult(IntEnum):
    SUCCESS = auto()
    STAY = auto()
    FAIL = auto()
    FAIL_AND_DAMAGE = auto()


CARD_TOOL = "T"
CARD_DEFAULT = "D"
CARD_PRODUCT = "PP"
CARD_OPTION = "PO"
CARD_MATERIA = "M"
