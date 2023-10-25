from __future__ import annotations
from dataclasses import dataclass, fields, field, asdict
from random import randint

import shortuuid


@dataclass(kw_only=True)
class CardTemplate:
    t: str
    c: int
    d: int = -1  # non discard-able card

    @property
    def can_discard(self):
        return self.d > 0

    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))

    def generate_same(self) -> Card:
        return Card(**asdict(self))

    def generate_variation(self, var_c: int = 10, var_d: int = 10) -> Card:
        return Card(t=self.t, c=modulate(self.c, var_c), d=modulate(self.d, var_d))

    def generate_variations(self, var_c: int = 10, var_d: int = 10, count=10) -> list[Card]:
        return [self.generate_variation(var_c, var_d) for i in range(count)]


@dataclass(kw_only=True)
class Card(CardTemplate):
    id: str = field(init=False)

    def __post_init__(self):
        self.id = f"{self.t}_{shortuuid.uuid()[:4]}"


reference_deck = []
active_deck = []

card_pool: dict[str, CardTemplate] = {}


def modulate(value, delta: int):
    variation = randint(0, delta)
    return value - delta // 2 + variation


def generate_variations(template: CardTemplate, count: int = 10, var_c: int = 10, var_d: int = 10):
    t, c, d = template
    return [Card(t=t, c=modulate(c, var_c), d=modulate(d, var_d)) for i in range(count)]
