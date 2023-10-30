from __future__ import annotations

import logging
from dataclasses import dataclass, field, InitVar
from random import randint, shuffle
from copy import copy
from loguru import logger

import typing as T

from simulators import RollResult
from simulators import CARD_PRODUCT, CARD_MATERIA, CARD_OPTION, CARD_DEFAULT
from simulators.cards import Card

ROLL_STAY = RollResult.STAY, 0
ROLL_FAIL = RollResult.FAIL, 0
ROLL_FAIL_AND_DAMAGE = RollResult.FAIL_AND_DAMAGE, 0
ROLL_SUCCESS_WITH_ENERGY = RollResult.SUCCESS, 1
ROLL_SUCCESS_NO_ENERGY = RollResult.SUCCESS, 0

logger.disable(__name__)


class GameSummary(T.NamedTuple):
    success: bool = False
    turn_count: int = 0
    project_size: int = 0
    project_to_build: int = 0
    lane_size: int = 0
    reserve_size: int = 0
    atelier_dm_resist: int =0
    optimist: bool = True
    damaged_slot_times: int = 0
    project_start_defaults_count: int = 0
    project_start_defaults_value: int = 0
    crafter_endurance: int = 0
    crafter_skill: int = 0
    max_energy: int = 0
    remaining_energy: int = 0
    constructed_count: int = 0
    overflowed_count: int = 0
    product_default_count: int = 0
    product_default_value: int = 0


def generate_cards_for_tpls(tpls: list[(Card, int)], var_delta: int | None = None):
    result = []
    sum_count = 0
    for tpl_record in tpls:
        tpl, count = tpl_record
        if var_delta is None:
            result.extend(tpl.generate_same() for i in range(count))
        else:
            result.extend(tpl.generate_variation(var_delta) for i in range(count))
        sum_count += count
    logger.info(
        "Generated {sum_count} cards for template {tpls}",
        sum_count=sum_count,
        tpls=tpls,
    )
    return result


@dataclass
class CardStack(list):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        result = list.__getitem__(self, key)
        if type(key) is slice:
            return type(self)(result)
        else:
            return result

    def __setitem__(self, index, item):
        super().__setitem__(index, item)

    def insert(self, index, item: Card):
        super().insert(index, item)

    def append(self, item: Card):
        super().append(item)

    def extend(self, other:T.Iterable):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(item for item in other)

    def shuffle(self):
        shuffle(self)

    def __repr__(self):
        return super().__repr__()

    def count_types(self, card_type: str) -> int:
        count: int = 0
        for card in self:
            if card.t == card_type:
                count += 1
        return count

    def filter_types(self, card_type: str) -> T.Iterator[Card]:
        yield from (card for card in self if card.t == card_type)


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

    def __post_init__(self):
        self.product_type_code = self.products_tpls[0][0].t
        self.product_goal = sum(tpl[1] for tpl in self.products_tpls)
        self.materia_goal = sum(tpl[1] for tpl in self.materias_tpls)
        self.materia_type_code = self.materias_tpls[0][0].t
        self.option_goal = sum(tpl[1] for tpl in self.options_tpls)

    def generate_deck(self) -> CardStack:
        cards: CardStack[Card] = CardStack()
        cards.extend(generate_cards_for_tpls(self.tools_tpls))
        cards.extend(generate_cards_for_tpls(self.products_tpls))
        cards.extend(generate_cards_for_tpls(self.materias_tpls))
        cards.extend(generate_cards_for_tpls(self.defaults_tpls))
        cards.extend(generate_cards_for_tpls(self.options_tpls))

        self.deck = cards
        logger.debug("Generated {} cards in deck", len(self.deck))
        return self.deck

    def check_total_success(self, stack: CardStack):
        product_count = stack.count_types(CARD_PRODUCT)
        material_count = stack.count_types(CARD_MATERIA)
        option_count = stack.count_types(CARD_OPTION)
        return (
            product_count == self.product_goal
            and material_count == self.materia_goal
            and self.option_goal == option_count
        )

    def check_partial_success(self, stack: CardStack):
        product_count = stack.count_types(CARD_PRODUCT)
        material_count = stack.count_types(CARD_MATERIA)
        return product_count == self.product_goal and material_count == self.materia_goal


@dataclass
class Lane:
    _size: int
    _slots: list[Card | None] = field(init=False)
    _slots_data: list[int] = field(init=False)  # for now only int total current bonuses

    def __post_init__(self, *args, **kwargs):
        self.setup()

    def setup(self):
        self._slots = list([None] * self._size)
        self._slots_data = list([0] * self._size)

    def __len__(self):
        return len(self._slots)

    def __str__(self):
        return " | ".join(f"{index}:{str(card)}" for index, card in enumerate(self._slots))

    def free_lane_space(self):
        return self._slots.count(None)

    def discard_overflow(self):
        self._slots, rejects = self._slots[: self._size], self._slots[self._size :]
        assert len(self._slots) == self._size
        return [r for r in rejects if r is not None]

    def __iter__(self) -> T.Iterator[Card | None]:
        return self._slots.__iter__()

    def __getitem__(self, key):
        return self._slots[key]

    def __setitem__(self, key, value):
        self._slots[key] = value

    def first_free_slot(self) -> int | None:
        try:
            return self._slots.index(None)
        except ValueError:
            return None

    def free_count(self) -> int:
        return self._slots.count(None)

    def add_card(self, card: Card, at_pos: int | None = None) -> list[Card]:  # or CardStack?
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

    def add_modifier(self, index, modifier):
        self._slots_data[index] += modifier

    def slot_modifier(self, index):
        return self._slots_data[index]


@dataclass
class Atelier:
    lane_size: InitVar[int]
    reserve_size: InitVar[int]
    _lane_size: int = field(init=False)
    _reserve_size: int = 0
    lane: Lane = field(init=False)
    reserve: Lane = field(init=False)
    damage_resistance: int = 0
    complexity: int = 0

    def __post_init__(self, lane_size, reserve_size):
        self._lane_size = lane_size
        self._reserve_size = reserve_size
        self.setup()

    def setup(self):
        self.lane = Lane(self._lane_size)
        self.reserve = Lane(self._reserve_size)

    @property
    def lane_size(self):
        return self._lane_size

    @lane_size.setter
    def lane_size(self, value):
        self._lane_size = value
        self.setup()

    @property
    def reserve_size(self):
        return self._reserve_size

    @reserve_size.setter
    def reserve_size(self, value):
        self._reserve_size = value
        self.setup()


@dataclass
class Crafter:
    craft_skill: int
    base_endurance: int
    current_endurance: int = field(init=False, default=0)
    base_skill_modifier: int = 0
    library: CardStack | None = field(default=None)

    def setup(self):
        self.current_endurance = self.base_endurance

    @property
    def effective_skill(self) -> int:
        return self.craft_skill + self.base_skill_modifier


ACTION_MODIFIER_COST = -10


@dataclass
class TurnData:
    modifier_value: int = field(init=False, default=0)

    # ToDo manage modifiers as instances to be able to explain and add / remove them individually

    def action_taken(self):
        self.modifier_value += ACTION_MODIFIER_COST

    def current_modifier(self):
        return self.modifier_value


@dataclass
class CraftGame:
    project: CraftProject
    atelier: Atelier
    crafter: Crafter
    crafter_hand: CardStack = field(default_factory=CardStack)
    _energy: int = field(init=False, default=0)
    max_energy: int = field(init=False, default=0)
    overflowed_count: int = 0
    generous_rolls: bool = True

    turn_count: int = field(init=False, default=0)
    _task_pile: CardStack | None = None
    default_stack: CardStack = field(default_factory=CardStack)
    constructed_stack: CardStack = field(default_factory=CardStack)
    _success: bool = field(init=False, default=False)
    # stats
    damaged_slot_times: int = field(init=False, default=0)
    game_summary: GameSummary = field(init=False, default_factory=GameSummary)

    def __post_init__(self):
        if len(self.project.deck) == 0:
            self.project.generate_deck()

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = value
        if self._energy > self.max_energy:
            self.max_energy = self._energy

    def setup_summary_base(self, game_summary: GameSummary) -> GameSummary:
        summary = game_summary._replace(
            success=self._success,
            turn_count=self.turn_count,
            lane_size=self.atelier.lane_size,
            reserve_size=self.atelier.reserve_size,
            atelier_dm_resist=self.atelier.damage_resistance,
            optimist=self.generous_rolls,
            project_to_build=self.project.product_goal + self.project.option_goal + self.project.materia_goal,
            project_start_defaults_count=self.project.deck.count_types(CARD_DEFAULT),
            project_start_defaults_value=sum(card.d for card in self.project.deck.filter_types(CARD_DEFAULT)),
            project_size=len(self.project.deck),  # wrong because we count_types product and materia defaults?
            crafter_endurance=self.crafter_current_endurance,
            crafter_skill=self.crafter.effective_skill,
            # max_energy=self.max_energy,
            # remaining_energy=self.energy,
            # damaged_slot_times=self.damaged_slot_times,
            # constructed_count=len(self.constructed_stack),
            # overflowed_count=self.overflowed_count,
            # product_default_count=len(self.default_stack),
            # product_default_value=sum(card.d for card in self.default_stack),
        )
        return summary

    @property
    def lane(self):
        return self.atelier.lane

    @property
    def reserve(self):
        return self.atelier.reserve

    @property
    def crafter_current_endurance(self):
        return self.crafter.current_endurance

    @crafter_current_endurance.setter
    def crafter_current_endurance(self, value):
        self.crafter.current_endurance = value

    def setup(self):
        self._success = False
        self.constructed_stack.clear()
        self.default_stack.clear()
        self._energy = 0
        self.max_energy = 0
        self.overflowed_count = 0
        self._task_pile = copy(self.project.deck)
        self._task_pile.shuffle()
        self.turn_count = 0
        self.damaged_slot_times = 0
        self.game_summary = self.setup_summary_base(self.game_summary)  # inelegant but we need to (re)init the summary


    def start(self):
        self.setup()
        # reset the production lane
        self.lane.setup()
        self.crafter.setup()

    def play_game(self) -> bool:
        logger.info("===========================================NEW GAME===========================================")
        while self.play_turn():
            # print(self.turn_count)
            if self.turn_count > 100:
                raise Exception("Too many turns ABORT ABORT")
        logger.info("===========================================GAME ENDED===========================================")
        return self._success

    def play_lane(self, lane: Lane, crafter: Crafter, turn_data: TurnData):
        """
        @TODO We need a more sophisticated strategy with the crafter hand and tools use.
        Args:
            turn_data:
            crafter:
            lane:

        Returns:

        """
        # we want to process the cards by order of increasing complexity
        indexes = list(range(self.atelier.lane_size))
        indexes.sort(key=lambda x: lane[x].c if lane[x] else 65535)
        for index in indexes:
            card = lane[index]
            if card:
                effective_skill = self.crafter.effective_skill + turn_data.modifier_value + lane.slot_modifier(index)
                logging.debug(f"turn {self.turn_count} slot {index} : card {card} | skill: {effective_skill}")
                result, energy = self.roll_card(effective_skill, card, self.generous_rolls)
                self.energy += energy
                match result:
                    case RollResult.FAIL:
                        logger.info("Crafter failed {card} failed test", card=card)
                        if not card.is_fixed:
                            logger.debug("moving Card {card} to defaults stack", card=card)
                            self.game_summary.product_default_count += 1
                            self.game_summary.product_default_value += card.d
                            self.default_stack.append(lane.remove_at(index))
                    case RollResult.SUCCESS:
                        logger.info(
                            "Crafter SUCCEEDED on {card} , moving it to constructed stack",
                            card=card,
                        )
                        self.constructed_stack.append(lane.remove_at(index))
                        self.game_summary.constructed_count += 1
                    case RollResult.STAY:
                        logger.debug("Card {card} STAYED in the lane", card=card)
                    case RollResult.FAIL_AND_DAMAGE:
                        malus = max(card.d - self.atelier.damage_resistance, 0)
                        self.game_summary.damaged_slot_times += 1
                        # malus = 0
                        if malus:
                            logger.error(
                                "Card {card} STAYED in the lane WITH DAMAGE {malus} to the SLOT",
                                card=card,
                                malus=malus,
                            )
                            lane.add_modifier(index, -malus)
                            self.damaged_slot_times += 1
                        else:
                            logger.info(
                                "Card {card} STAYED in the lane with damage to the SLOT, but it resisted !!",
                                card=card,
                            )

                    case _:
                        raise NotImplementedError
                turn_data.action_taken()
                logger.debug("Turn modifier is now : {}", turn_data.modifier_value)

    def play_turn(self) -> bool:
        self.turn_count += 1
        logger.info(
            "__________________________________new turn {}__________________________________",
            self.turn_count,
        )
        turn_data = TurnData()
        # lose endurance
        self.crafter_current_endurance -= 1
        # pick cards
        how_many_max = self.lane.free_count()
        # we randomize the crafter decision with a margin of two
        if len(self._task_pile):
            nb_pick = max(how_many_max - randint(0, 2), 0)
            logger.debug("Retrieving {} tasks", nb_pick)
            if nb_pick == 0:
                hand = []
            else:
                hand, self._task_pile = (
                    self._task_pile[-nb_pick:],
                    self._task_pile[:-nb_pick],
                )
                logger.debug("Picked up hand => {hand}", hand=hand)
                overflow = self.lane.add_cards(hand)
                if overflow:
                    # check if overflow contains a loosing condition?
                    self.default_stack.extend(overflow)
                    logger.critical(f"overflow of the main lane  => {overflow}", overflow=overflow)
        else:
            logger.info("Task pile is empty")
        # resolve lanes
        self.play_lane(self.atelier.lane, self.crafter, turn_data)
        # check possible partial success
        # @TODO

        # check loss
        if self.crafter_current_endurance <= 0 or (len(self._task_pile) == 0 and len(self.lane) == 0):
            return False
        # check complete success
        self._success = self.project.check_total_success(self.constructed_stack)
        return not self._success

    def roll_card(self, skill, card: Card, optimist=True) -> (RollResult, int):
        """
        Simulates rolling dice to determine the outcome of playing a card.

        Parameters:
        - skill: The skill level of the crafter
        - card: The Card object being played
        - optimist: Whether to use optimistic rules (default True)

        Returns:
        - A tuple containing:
          - The RollResult enum value
          - The amount of energy used/gained

        The method generates two random numbers between 1-100 to represent an
        "art roll" and "complexity roll".

        It compares the skill level to the art roll, and the card's complexity
        to the complexity roll.

        Based on the success/failure of these rolls, it returns one of the
        RollResult enums:

        - ROLL_SUCCESS_NO_ENERGY: Passed both rolls
        - ROLL_SUCCESS_WITH_ENERGY: Passed art roll but not complexity roll
        - ROLL_FAIL: Failed art roll but passed complexity roll
        - ROLL_FAIL_AND_DAMAGE: Failed both rolls, damage to lane
        - ROLL_STAY: Failed complexity roll but passed art roll

        The optimist flag determines ROLL_STAY vs ROLL_FAIL when only failing
        complexity.
        """

        complexity = card.c
        roll_art = randint(1, 100)
        roll_slot = randint(1, 100)
        art_pass = skill >= roll_art
        c_pass = complexity >= roll_slot
        # Dumb version of the automatic rule
        if skill > complexity:
            return ROLL_SUCCESS_NO_ENERGY
        if skill < complexity-20:
            logger.debug(f"skill {skill} very much below complexity {complexity}, not risking it ")
            return ROLL_STAY
        if art_pass and c_pass:
            if roll_art > roll_slot:
                return ROLL_SUCCESS_NO_ENERGY
            else:
                return ROLL_STAY if optimist else ROLL_FAIL
        if art_pass and not c_pass:
            return ROLL_SUCCESS_WITH_ENERGY
        if not art_pass and c_pass:
            return ROLL_FAIL
        assert not art_pass and not c_pass
        if roll_slot > roll_art:  # Damage to the lane
            return ROLL_FAIL_AND_DAMAGE
        return ROLL_STAY
