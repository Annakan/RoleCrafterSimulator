from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from random import randint, choice, choices, shuffle
from copy import copy, deepcopy

import typing as T
from typing import List, Any

from simulators import RollResult

from simulators.cards import Card


def generate_cards_for_tpls(tpls: list[(Card, int)], var_delta: int | None = None):
    result = []
    for tpl_record in tpls:
        tpl, count = tpl_record
        if var_delta is None:
            result.extend(tpl.generate_same() for i in range(count))
        else:
            result.extend(tpl.generate_variation(var_delta) for i in range(count))
    return result


@dataclass
class CardStack(list):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

    def __setitem__(self, index, item):
        super().__setitem__(index, item)

    def insert(self, index, item):
        super().insert(index, item)

    def append(self, item):
        super().append(item)

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(item for item in other)

    def shuffle(self):
        shuffle(self)

    def __repr__(self):
        return super().__repr__()

    # def __len__(self):
    #     return len(self.cards)
    #
    # def __getitem__(self, item):
    #     return self.cards.__getitem__(item)
    #
    # def extend(self):

    def count(self, card_type: str):
        count: int = 0
        for card in self:
            if card.t == card_type:
                count += 1
        return count
    #
    # def copy(self):
    #     return copy(self)
    #
    # def clone(self):
    #     return deepcopy(self)


@dataclass
class CraftProject:
    materias_tpls: list[(Card, int)] = field(default_factory=list)
    products_tpls: list[(Card, int)] = field(default_factory=list)
    options_tpls: list[(Card, int)] = field(default_factory=list)
    defaults_tpls: list[(Card, int)] = field(default_factory=list)
    tools_tpls: list[(Card, int)] = field(default_factory=list)
    deck: CardStack = field(init=False, default_factory=CardStack)
    product_goal: (str, int) = field(init=False)
    materia_goal: int = field(init=False)
    option_goal: int = field(init=False)
    product_type_code: str = field(init=False, default="")
    materia_type_code: str = field(init=False, default="")
    option_type_code: str = field(init=False, default="")

    def __post_init__(self):
        self.product_type_code = self.products_tpls[0][0].t
        self.product_goal = sum(tpl[1] for tpl in self.products_tpls)
        self.materia_goal = sum(tpl[1] for tpl in self.materias_tpls)
        self.materia_type_code = self.materias_tpls[0][0].t
        self.option_goal = sum(tpl[1] for tpl in self.options_tpls)
        if self.option_goal:
            self.option_type_code = self.options_tpls[0][0].t

    def generate_deck(self) -> CardStack:
        cards: CardStack[Card] = CardStack()
        cards.extend(generate_cards_for_tpls(self.tools_tpls))
        cards.extend(generate_cards_for_tpls(self.products_tpls))
        cards.extend(generate_cards_for_tpls(self.materias_tpls))
        cards.extend(generate_cards_for_tpls(self.defaults_tpls))
        cards.extend(generate_cards_for_tpls(self.options_tpls))

        self.deck = cards
        return self.deck

    def check_total_success(self, stack: CardStack):
        product_count = stack.count(self.product_type_code)
        material_count = stack.count(self.materia_type_code)
        option_count = stack.count(self.option_type_code) if self.option_goal else 0
        return (product_count == self.product_goal
                and material_count == self.materia_goal
                and self.option_goal == option_count)

    def check_partial_success(self, stack: CardStack):
        product_count = stack.count(self.product_type_code)
        material_count = stack.count(self.materia_type_code)
        return (product_count == self.product_goal
                and material_count == self.materia_goal)


@dataclass
class Lane:
    _size: int
    _slots: list[Card | None] = field(init=False)

    def __post_init__(self):
        self._slots = list([None] * self._size)

    def __len__(self):
        return len(self._slots)

    def __str__(self):
        return ' | '.join(f"{index}:{str(card)}" for index, card in enumerate(self._slots))

    def free_lane_space(self):
        return self._slots.count(None)

    def discard_overflow(self):
        self._slots, rejects = self._slots[:self._size], self._slots[self._size:]
        assert len(self._slots) == self._size
        return [r for r in rejects if r is not None]

    def __iter__(self) -> T.Iterator[Card | None]:
        return self._slots.__iter__()

    def first_free_slot(self) -> int | None:
        try:
            return self._slots.index(None)
        except ValueError:
            return None

    def free_count(self) -> int:
        return self._slots.count(None)

    def add_card(self, card: Card, at_pos: int | None = None) -> list[Card]:  # or CardStack ?
        if at_pos is None:
            if (free_slot := self.first_free_slot()) is not None:
                self._slots[free_slot] = card
            else:  # this card will be discarded (see last line)
                self._slots.append(card)
        else:
            if at_pos >= self._size:
                self._slots.append(card)  # this card will be discarded (see last line)
            else:
                card_at_pos = self._slots[at_pos]
                if card_at_pos is None:
                    self._slots[at_pos] = card
                elif card_at_pos.is_fixed:
                    return self.add_card(card, at_pos + 1)
                else:
                    self._slots[at_pos] = card
                    return self.add_card(card_at_pos, at_pos + 1)

        return self.discard_overflow()

    def add_cards(self, cards: list[Card] | CardStack):
        overflow = []
        for card in cards:
            overflow.extend(self.add_card(card))
        return overflow

    def remove_at(self, index: int) -> Card:
        removed = self._slots[index]
        self._slots[index] = None
        return removed

    def at_pos(self, index: int) -> Card:
        return self._slots[index]


@dataclass
class Atelier:
    lane_size: int
    reserve_size: int
    lane: Lane = field(init=False)
    reserve: Lane = field(init=False)

    def __post_init__(self):
        self.lane = Lane(self.lane_size)
        self.reserve = Lane(self.reserve_size)


@dataclass
class CraftGame:
    project: CraftProject
    atelier: Atelier
    craft_endurance: int
    craft_skill: int
    energy: int = field(init=False, default=0)
    generous_rolls: bool = True

    turn_count: int = field(init=False, default=0)
    _task_pile: CardStack | None = None
    default_stack: CardStack = field(default_factory=CardStack)
    constructed_stack: CardStack = field(default_factory=CardStack)
    _success: bool = field(init=False, default=False)
    _failure: bool = field(init=False, default=False)

    def __post_init__(self):
        if len(self.project.deck) == 0:
            self.project.generate_deck()

    def summary(self):
        return (self.turn_count, self._success, self._failure, self.craft_endurance,
                self.craft_skill, len(self.constructed_stack), len(self.default_stack))

    @property
    def lane(self):
        return self.atelier.lane

    @property
    def reserve(self):
        return self.atelier.reserve

    def start(self):
        self._task_pile = copy(self.project.deck)

    def play_game(self):
        while self.play_turn():
            # print(self.turn_count)
            if self.turn_count > 100:
                raise Exception("Too many turns ABORT ABORT")

    def play_lane(self, lane: Lane):
        """
        @TODO We need a more sophisticated strategy with the crafter hand and tools use.
        Args:
            lane:

        Returns:

        """
        for index, card in enumerate(lane):
            if card:
                result, energy = self.roll_card(self.craft_skill, card, self.generous_rolls)
                self.energy += energy
                match result:
                    case RollResult.FAIL:
                        if not card.is_fixed:
                            self.default_stack.append(lane.remove_at(index))
                    case RollResult.SUCCESS:
                        self.constructed_stack.append(lane.remove_at(index))
                    case RollResult.FAIL:
                        pass

    def play_turn(self) -> bool:
        self.turn_count += 1
        # pick cards
        self.craft_endurance -= 1
        how_many_max = self.lane.free_count()
        # print(f"free lanes {how_many_max}")
        # print(f"task_pile = {len(self._task_pile)}")
        # we randomize with a margin of two
        nb_pick = randint(how_many_max - 2, how_many_max)
        hand, self._task_pile = self._task_pile[-nb_pick:], self._task_pile[:-nb_pick]
        overflow = self.lane.add_cards(hand)
        # check if overflow contains a loosing condition?
        self.default_stack.extend(overflow)
        # resolve lanes
        self.play_lane(self.atelier.lane)
        # check possible partial success
        # @TODO

        # check loss
        if self.craft_endurance <= 0 or len(self._task_pile) == 0:
            self._failure = True
            return False
        # check complete success
        self._success = self.project.check_total_success(self.constructed_stack)
        return not self._success

    def roll_card(self, skill, card: Card, optimist=True) -> (RollResult, int):
        energy_gain = 0
        complexity = card.c
        skill = self.craft_skill
        r1 = randint(1, 100)
        r2 = randint(1, 100)
        art_pass = (skill >= r1)
        c_pass = (complexity >= r2)
        if art_pass and c_pass:
            if r1 > r2:
                return RollResult.SUCCESS, 0
            else:
                return (RollResult.STAY, 0) if optimist else (RollResult.FAIL, 0)
        if art_pass and not c_pass:
            return RollResult.SUCCESS, 1
        if not art_pass and c_pass:
            return RollResult.FAIL, 0
        return RollResult.STAY, 0
