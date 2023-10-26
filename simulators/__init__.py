from enum import Enum, auto, IntEnum


class RollResult(IntEnum):
    SUCCESS = auto()
    STAY = auto()
    FAIL = auto()
