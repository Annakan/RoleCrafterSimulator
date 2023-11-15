from random import randint
from collections import Counter
from enum import Enum, auto, IntEnum
import typing as T
from simulators import RollResult
from math import pow


def roll(art_skill, card_complexity, crit_a=None, crit_c=None):
    if crit_a is None:
        crit_a = art_skill // 10
    if crit_c is None:
        crit_c = card_complexity // 10
    art_roll = randint(1, 100)
    card_roll = randint(1, 100)
    print(f"A:{art_roll} |  C:{card_roll}", end="")

    art_pass = (95 > art_roll <= art_skill)
    art_has_crit = (art_roll <= crit_a)
    card_pass = (95 > card_roll < card_complexity)
    card_has_crit = (card_roll <= crit_c)

    art_fumble = True if (art_roll in (99, 100) and art_skill <= 100) else art_roll == 100
    card_fumble = True if (card_roll in (99, 100) and card_complexity <= 100) else card_roll == 100
    #
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
    return RollResult.STAY


# simulation grossière de la main

c = Counter()

skill = 85
# skill_crit = skill // 10
skill_crit = 10

card_complexity = 75
# card_crit = card_complexity // 10
card_crit = 7

count = 200
# lane_size = 3

rolls = []
for _ in range(0, count):
    r = roll(skill, card_complexity, crit_c=card_crit, crit_a=skill_crit)
    rolls.append(r)
    print(f" {r.name}")

c.update(rolls)
print(sorted([(i, round(c[i] / c.total() * 100.0, 2)) for i in c]))

if skill >= card_complexity:
    calculated = ((pow(skill, 2)  # skill square
                   - (pow(card_complexity, 2) / 2)  # card complexity triangle
                   + ((pow(skill_crit, 2) / 2) - pow(card_crit,
                                                     2) / 2)  # size art crit zone lower triangle minus card crit triangle
                   - ((skill - skill_crit) * card_crit)  # card crit rectangle
                   + (card_complexity - skill_crit) * skill_crit)  # art crit rectangle
                  / 10000)
    print(calculated * 100)
    calculated3 = ((skill * skill) - card_crit * (skill - skill_crit) - pow(card_complexity - skill_crit, 2) / 2 - pow(
        card_crit, 2) / 2) / 100
    print(calculated3)
