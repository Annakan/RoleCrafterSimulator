from enum import Enum, auto, IntEnum


class RollResult(IntEnum):
    SUCCESS = auto()
    STAY = auto()
    FAIL = auto()
    FAIL_AND_DAMAGE = auto()


CARD_TOOL = "T"
DEFAULT_CARD_CODE = "D"
PRODUCT_CARD_CODE = "PP"
OPTION_CARD_CODE = "PO"
MATERIA_CARD_CODE = "M"
