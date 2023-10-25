from random import randint
from collections import Counter
from enum import Enum, auto, IntEnum
import typing as T


class Result(IntEnum):
    SUCCESS = auto()
    STAY = auto()
    FAIL = auto()


def roll_pos(skill, complexity):
    r1 = randint(1, 100)
    r2 = randint(1, 100)
    art_pass = (skill >= r1)
    c_pass = (complexity >= r2)
    if art_pass and c_pass:
        if r1 > r2:
            return Result.SUCCESS
        else:
            return Result.STAY
    if art_pass and not c_pass:
        return Result.SUCCESS
    if not art_pass and c_pass:
        return Result.FAIL
    return Result.STAY


def roll_pess(skill, complexity):
    r1 = randint(1, 100)
    r2 = randint(1, 100)
    art_pass = (skill >= r1)
    c_pass = (complexity >= r2)
    if art_pass and c_pass:
        if r1 > r2:
            return Result.SUCCESS
        else:
            return Result.FAIL
    if art_pass and not c_pass:
        return Result.SUCCESS
    if not art_pass and c_pass:
        return Result.FAIL
    return Result.STAY


# simulation grossière de la main

c = Counter()

skill = 95
complexity = 65
count = 2000
file_size = 3

for turn in range(0, count):
    rolls = [roll_pos(skill - i * 10, complexity) for i in range(0, file_size)]
    c.update(rolls)
print(c)
sorted([(i, round(c[i] / c.total() * 100.0, 2)) for i in c])
