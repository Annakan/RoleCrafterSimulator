from dataclasses import dataclass, Field
from random import randint, choice, choices
import typing as T


@dataclass
class Card:
    type: str
    complexity: int
    default_value: int


reference_deck = []
active_deck = []

card_pool: dict[str, Card] = {}

materia_card_template_L1 = Card("materia1", 40, 40)
materia_card_template_L2 = Card("materia1", 50, 50)
materia_card_template_L3 = Card("materia1", 70, 70)
materia_card_template_L4 = Card("materia1", 90, 90)
materia_card_template_L5 = Card("materia1", 100, 100)

def modulate(value, delta:int):
    variation = randint(0, delta)
    return value-delta//2+variation


def generate_variations(template: Card, count:int=10, var_c:int=10, var_d:int=10):
    name, c, d = template
    return [Card(name, modulate(c,var_c), modulate(d, var_d)) for i in range(count)]

