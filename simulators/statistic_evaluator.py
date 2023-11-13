from random import randint
from collections import Counter
from enum import Enum, auto, IntEnum
import typing as T
from simulators import RollResult
from math import pow


def roll(skill, complexity, crit_s=None, crit_c=None):
    if crit_s is None:
        crit_s = skill // 10
    if crit_c is None:
        crit_c = complexity // 10
    art_roll = randint(1, 100)
    card_roll = randint(1, 100)
    art_pass = (95 > art_roll <= skill)
    art_has_crit = (art_roll <= crit_s)
    card_pass = (95 > card_roll < complexity)
    card_has_crit = (card_roll <= crit_c)
    art_fumble = True if (art_roll in (99, 100) and skill <= 100) else art_roll == 100
    card_fumble = True if (card_roll in (99, 100) and complexity <= 100) else card_roll == 100
    if art_fumble and card_pass:
        return RollResult.FAIL_AND_DAMAGE
    if art_fumble and card_fumble:
        return RollResult.FAIL_AND_DAMAGE if card_roll > art_roll else RollResult.STAY
    if art_has_crit and not card_has_crit:
        # print("+", end="")
        return RollResult.SUCCESS
    if card_has_crit and not art_has_crit:
        # print("-", end="")
        return RollResult.FAIL

    if art_has_crit and card_has_crit:
        if art_roll > card_roll:
            return RollResult.SUCCESS
        else:
            return RollResult.STAY
    if art_pass and card_pass:
        assert art_roll < 96 and card_roll < 96
        if art_roll > card_roll:
            return RollResult.SUCCESS
        else:
            return RollResult.STAY
    if art_pass and not card_pass:
        return RollResult.SUCCESS
    if not art_pass and card_pass:
        return RollResult.FAIL
    assert not art_pass and not card_pass
    return RollResult.FAIL


# simulation grossière de la main

c = Counter()

skill = 90
card_complexity = 75
skill_crit = skill // 10
card_crit = card_complexity // 10
count = 100000
# file_size = 3

rolls = [roll(skill, card_complexity, crit_c=card_crit, crit_s=skill_crit) for _ in range(0, count)]
c.update(rolls)
print(c)
print(sorted([(i, round(c[i] / c.total() * 100.0, 2)) for i in c]))
if skill >= card_complexity:
    calculated = (pow(skill, 2) - (pow(card_complexity, 2) / 2) - ((skill - skill_crit) * card_crit)) / 10000
    print(calculated * 100)
    calculated2 = (skill * skill / 2 + (skill - card_complexity) * skill - pow(skill - card_complexity, 2) / 2 - (
                (skill - skill_crit) * card_crit)) / 10000
    print(calculated2 * 100)
