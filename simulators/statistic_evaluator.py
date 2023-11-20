from random import randint
from collections import Counter
from simulators import RollResult
from math import pow, trunc

import typing as T


class RollRecord(T.NamedTuple):
    art_roll: int
    card_roll: int
    roll_result: RollResult


class RollChances(T.NamedTuple):
    skill: int
    complexity: int
    win: float
    stay: float = 0
    fail: float = 0
    damage: float = 0

    def _as_percent_dict(self):
        return RollChances(
            self.skill,
            self.complexity,
            (self.win * 100),
            (self.stay * 100),
            (self.fail * 100),
            (self.damage * 100)
        )


def _roll_result(
        art_roll, card_roll, art_pass, art_has_crit, card_pass, card_has_crit, art_fumble, card_fumble
) -> RollResult:
    #
    if art_fumble and card_pass:
        return RollResult.FAIL_AND_DAMAGE
    if art_fumble and card_fumble:
        return RollResult.FAIL_AND_DAMAGE if card_roll > art_roll else RollResult.STAY
    if card_has_crit and not art_pass:
        return RollResult.FAIL_AND_DAMAGE
    if art_has_crit and not card_has_crit:
        # print("+", end="")
        return RollResult.SUCCESS
    if card_has_crit and not art_has_crit:
        assert art_pass
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
    roll_result = RollResult.STAY
    return roll_result


def roll(art_skill, card_complexity, crit_a=None, crit_c=None, art_roll=None, card_roll=None) -> RollRecord:
    if crit_a is None:
        crit_a = art_skill // 10
    if crit_c is None:
        crit_c = card_complexity // 10
    art_roll = randint(1, 100) if art_roll is None else art_roll
    card_roll = randint(1, 100) if card_roll is None else card_roll
    # print(f"A:{art_roll} |  C:{card_roll}", end="")
    art_pass = 95 > art_roll <= art_skill
    art_has_crit = art_roll <= crit_a
    card_pass = 95 > card_roll < card_complexity
    card_has_crit = card_roll <= crit_c

    art_fumble = True if (art_roll in (99, 100) and art_skill <= 100) else art_roll == 100
    card_fumble = True if (card_roll in (99, 100) and card_complexity <= 100) else card_roll == 100

    roll_result = _roll_result(
        art_roll, card_roll, art_pass, art_has_crit, card_pass, card_has_crit, art_fumble, card_fumble
    )
    return RollRecord(art_roll, card_roll, roll_result)


def computed_chances(art_skill, card_complexity, art_crit=None, card_crit=None) -> RollChances:
    if art_crit is None:
        art_crit = art_skill // 10
    if card_crit is None:
        card_crit = card_complexity // 10
    if art_skill >= card_complexity:
        win = (
                (
                        (art_skill * (100 - card_crit))  # art_skill rectangle
                        - (card_complexity - art_crit) * (card_complexity - art_crit) / 2

                        + ((art_crit * card_crit) - (pow(card_crit, 2) / 2) if art_crit > card_crit else (
                        pow(card_crit, 2) / 2))  # card crit rectangle
                )  # art crit rectangle
                / 10000
        )
        base_stay = (100 - card_complexity) * (100 - art_skill)
        if card_crit > art_crit:
            base_stay += pow(card_complexity, 2) / 2
            base_stay -= pow(card_crit-art_crit, 2) / 2
            base_stay -= (card_complexity-card_crit) * art_crit
        else:
            base_stay += pow(card_complexity-art_crit, 2)/2
            base_stay += pow(card_crit, 2) / 2
        stay = base_stay / 10000
        fail = ((card_complexity - card_crit) * (98 - art_skill) + (card_crit * (art_skill - art_crit))) / 10000
        damage = ((100 - art_skill) * card_crit + (2 * (card_complexity - card_crit))) / 10000

    else:
        if card_crit > art_crit:
            base_win = (100 - card_complexity) * art_skill
            base_win += pow(art_skill - card_crit, 2) / 2
            base_win += (card_complexity - card_crit) * art_crit
        else:
            base_win = 100 * art_skill
            base_win -= (card_complexity - art_skill) * (art_skill-art_crit)
            base_win -= pow(art_skill - art_crit, 2) / 2
            base_win -= (art_skill - art_crit) * card_crit
            base_win -= pow(card_crit, 2) / 2
        # win = (
        #
        #               + (card_complexity - card_crit) * art_crit
        #               + pow(card_crit, 2) / 2
        #               + pow(art_skill - card_crit, 2) / 2
        #       ) / 10000
        win = base_win / 10000
        base_stay = (100 - card_complexity) * (100 - art_skill)
        if card_crit > art_crit:
            base_stay += (card_complexity - card_crit) * (art_skill - art_crit) - pow(art_skill - card_crit, 2) / 2
            base_stay += card_crit * art_crit - pow(art_crit, 2) / 2
        else:
            base_stay += (card_complexity - art_crit) * (art_skill - art_crit) - pow(art_skill - art_crit, 2) / 2
            base_stay -= pow(card_crit, 2) / 2
        stay = base_stay / 10000
        fail = ((card_complexity - card_crit) * (98 - art_skill) + (card_crit * (art_skill - art_crit))) / 10000
        damage = ((100 - art_skill) * card_crit + (2 * (card_complexity - card_crit))) / 10000

    return RollChances(art_skill, card_complexity, win, stay, fail, damage)


# simulation grossière de la main
def roll_a_lot(skill, card_complexity, skill_crit, card_crit, count) -> list[RollRecord]:
    rolls = []
    for _ in range(0, count):
        r = roll(skill, card_complexity, crit_c=card_crit, crit_a=skill_crit)
        rolls.append(r)
        # print(f" {r.roll_result.name}")
    return rolls


def main():
    skill = 95
    # art_crit = art_skill // 10
    skill_crit = 6

    card_complexity = 60
    # card_crit = card_complexity // 10
    card_crit = 6

    count = 800000
    # lane_size = 3

    c = Counter()

    rolls = roll_a_lot(
        skill=skill, card_complexity=card_complexity, skill_crit=skill_crit, card_crit=card_crit, count=count
    )
    c.update(r.roll_result for r in rolls)
    estimated_stats = sorted([(i, round(c[i] / c.total() * 100.0, 2)) for i in c])
    print(f"Estimated : {estimated_stats}")
    cc = computed_chances(art_skill=skill, card_complexity=card_complexity, art_crit=skill_crit, card_crit=card_crit)
    print(f"Computer success chances : {cc._as_percent_dict()}")


if __name__ == "__main__":
    main()
