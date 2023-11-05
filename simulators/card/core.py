from __future__ import annotations
from dataclasses import dataclass, fields, asdict
from random import randint
from loguru import logger

import shortuuid

import typing as T

if T.TYPE_CHECKING:
    from simulators.refined_simulator import VisibleGameState
    from simulators.game_state import CardId


@dataclass(kw_only=True)
class CardTemplate:
    t: str  # type
    l: int  # level
    c: int  # complexity
    d: int | None = None  # non discard-able card
    _fixed: bool = False

    def __post_init__(self):
        if self.d is None:
            self.d = self.c

    @property
    def can_discard(self):
        return self.d > 0

    @property
    def is_fixed(self):
        return self._fixed

    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))

    def generate_same(self, cid: str | None = None) -> Card:
        return Card(cid=cid, **asdict(self))

    def generate_variation(self, var_c: int = 10, var_d: int = 10) -> Card:
        return Card(
            t=self.t,
            l=self.l,
            c=modulate(self.c, var_c),
            d=modulate(self.d, var_d) if self.can_discard else self.d,
        )

    def generate_variations(
            self, var_c: int = 10, var_d: int = 10, count=10
    ) -> list[Card]:
        return [self.generate_variation(var_c, var_d) for i in range(count)]


@dataclass(kw_only=True)
class Card(CardTemplate):  # @TODO remove the hierarchy dependency
    _CardID: CardId = None

    def __post_init__(self):
        if self.cid is None:
            self.cid = f"{self.t}_{shortuuid.uuid()[:4]}"
        else:
            self.cid = f"{self.cid}_{shortuuid.uuid()[:4]}"

    def __str__(self):
        return f"self.cid|Lvl:{self.l}|c:{self.c}|d:{self.d}"

    def can_play(self, state: VisibleGameState) -> bool:
        raise NotImplementedError

    def play(self, state: VisibleGameState) -> VisibleGameState:
        raise NotImplementedError


    @classmethod
    def card_id(cls) -> CardId:
        card_id = cls._CardID
        if card_id is not None:
            return cls._CardID.rsplit(':', 1)[0] if card_id.count(':') > 1 else card_id
        return None


@dataclass(kw_only=True)
class ToolCard(Card):
    """Represents cards that stay on the lane and are installed by the crafter."""
    pass


@dataclass(kw_only=True)
class DifficultyCard(Card):
    """Represents cards that are difficulties to be handled by the crafer to succeed in its craft."""
    pass


@dataclass(kw_only=True)
class CrafterCard(Card):
    """
    Represent Cards that are in the hand of the crafter. Available to be played.
    """
    pass


@dataclass(kw_only=True)
class TemplateCard(Card):
    """
    Represents Cards that are "instances" of a template, they are conditions for "success"²
    """
    pass


@dataclass(kw_only=True)
class MainTemplateCard(Card):
    """
    Represent cards that are the instances of the main template for the craft.
    Those cards need to be all built for the Craft to be successful.

    """
    pass


@dataclass(kw_only=True)
class OptionTemplateCard(Card):
    """
    Represent cards that are the instances of an optionnal template for the craft.
    Those cards need not be all built for the Craft to be successful.
    """
    pass


@dataclass(kw_only=True)
class MaterialCard(TemplateCard):
    """
    Represent cards that are the instances of the material template associated with the MainTemplate for the craft.
    Those cards need to be all built for the Craft to be successful.

    """
    pass


card_pool: dict[str, CardTemplate] = {}


def modulate(value, delta: int):
    variation = randint(0, delta)
    return value - delta // 2 + variation


def generate_variations(
        template: CardTemplate, count: int = 10, var_c: int = 10, var_d: int = 10
):
    t, c, d = template
    return [Card(t=t, c=modulate(c, var_c), d=modulate(d, var_d)) for i in range(count)]


def card_factory(card_id: CardId):
    """
    Instanciate the proper card from the right class based on the card_id.
    class for special cards need to register themselves in the card_registry.
    if a card_id is not in the registry, it is replaced by a generic card with a log message.
    Args:
        card_id:

    Returns:

    """


__card_registry: dict[CardId: type[Card]] = {}


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def populate_registry():
    for klass in all_subclasses(Card):
        logger.info(f"found card {klass}")
        card_id = klass.card_id()
        __card_registry[card_id] = klass
        if card_id is None:
            logger.warning(f"{klass} card_is id None")
        else:
            logger.info(f"{klass} card_is is {card_id}")
